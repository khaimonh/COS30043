import asyncio, logging, os
from sqlalchemy import select, exists
from api.database import AsyncSessionLocal
from api.models import Stock, PriceHistory, Watchlist, Holding
from api.services.redis_service import (
    get_redis,
    set_quote_with_timestamp,
    publish_quote,
    get_latest_history_batch,
)
from api.services.stock_service import get_market_snapshot

logger = logging.getLogger("price_poller")

POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "10"))
PRICE_TTL_SECONDS = int(os.getenv("PRICE_TTL_SECONDS", "15"))

QUOTE_DELAY_SECONDS = 3.1

class PricePoller:
    def __init__(self):
        self._seed_task: asyncio.Task | None = None
        self._task: asyncio.Task | None = None
        self.redis_client=get_redis()

    async def start(self):
        self._seed_task = asyncio.create_task(self._seed_redis(), name="price-poller-seed")
        self._task = asyncio.create_task(self._run_forever(), name="price-poller")

    async def stop(self):
        for task in (self._seed_task, self._task):
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    async def _seed_redis(self):
        """Prime Redis from persisted history so it isn't cold at startup.

        Runs as a background task — live ticks overwrite these historical
        values within one poll cycle, and the PriceHistory fallback covers
        requests that land before seeding finishes.
        """
        async with AsyncSessionLocal() as session:
            rows = (
                await session.execute(
                    select(Stock.stock_id, Stock.ticker)
                    .where(Stock.listed == True)
                    .where(
                        exists(select(1).where(Watchlist.stock_id == Stock.stock_id))
                        | exists(select(1).where(Holding.stock_id == Stock.stock_id))
                    )
                )
            ).all()
            stock_ids = [stock_id for stock_id, _ in rows]
            if not stock_ids:
                return
            latest = await session.run_sync(get_latest_history_batch, stock_ids)
            for stock_id, ticker in rows:
                entry = latest.get(stock_id)
                if not entry:
                    continue
                price, recorded_at = entry
                ts_ms = int(recorded_at.timestamp() * 1000)
                try:
                    await set_quote_with_timestamp(
                        self.redis_client, ticker, {"close_price": str(price)}, ts_ms=ts_ms
                    )
                except Exception as e:
                    logger.warning("seed redis failed for %s: %s", ticker, e)

    async def _run_forever(self):
        while True:
            try:
                await self.run_once()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("poll cycle failed")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)

    async def run_once(self):
        async with AsyncSessionLocal() as session:
            rows = (
                await session.execute(
                    select(Stock.stock_id, Stock.ticker)
                    .where(Stock.listed == True)
                    .where(
                        exists(select(1).where(Watchlist.stock_id == Stock.stock_id))
                        | exists(select(1).where(Holding.stock_id == Stock.stock_id))
                    )
                )
            ).all()
            for stock_id, ticker in rows:
                try:
                    data = await asyncio.to_thread(get_market_snapshot, ticker)
                    close_price = data.get("close_price")
                except (Exception, SystemExit) as e:
                    # vnstock raises SystemExit on rate limit; don't let it kill the API process
                    logger.warning("quote fetch failed for %s: %s", ticker, e)
                    await asyncio.sleep(QUOTE_DELAY_SECONDS)
                    continue
                if not close_price:
                    logger.warning("no close_price for %s", ticker)
                    await asyncio.sleep(QUOTE_DELAY_SECONDS)
                    continue

                try:
                    ts_ms = await set_quote_with_timestamp(self.redis_client, ticker, data)
                    await publish_quote(self.redis_client, ticker, data, ts_ms)
                except Exception as e:
                    logger.warning("redis set failed for %s: %s", ticker, e)
                session.add(PriceHistory(
                    stock_id=stock_id,
                    price=close_price,
                    open_price=data.get("open_price"),
                    high_price=data.get("high_price"),
                    low_price=data.get("low_price"),
                    volume=data.get("volume_accumulated"),
                ))
                await asyncio.sleep(QUOTE_DELAY_SECONDS)
            try:
                await session.commit()
            except Exception:
                logger.exception("price_history commit failed")
                await session.rollback()