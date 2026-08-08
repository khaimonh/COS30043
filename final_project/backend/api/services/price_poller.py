import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import select, exists
from api.database import AsyncSessionLocal
from api.models import Stock, PriceHistory, Watchlist, Holding
from api.services.redis_service import (
    get_redis,
    set_quote_with_timestamp,
    publish_quote,
    get_latest_history_batch,
)
from api.services.stock_service import fetch_quotes_bulk

logger = logging.getLogger("price_poller")

POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "10"))
PRICE_TTL_SECONDS = int(os.getenv("PRICE_TTL_SECONDS", "15"))
COLD_POLL_INTERVAL_SECONDS = float(os.getenv("COLD_POLL_INTERVAL_SECONDS", "300"))
COLD_TTL_SECONDS = int(os.getenv("COLD_TTL_SECONDS", "900"))

class PricePoller:
    def __init__(self):
        self._seed_task: asyncio.Task | None = None
        self._task: asyncio.Task | None = None
        self._cold_task: asyncio.Task | None = None
        self.redis_client=get_redis()

    async def start(self):
        self._seed_task = asyncio.create_task(self._seed_redis(), name="price-poller-seed")
        self._task = asyncio.create_task(self._run_forever(), name="price-poller")
        self._cold_task = asyncio.create_task(self._run_cold_forever(), name="price-poller-cold")

    async def stop(self):
        for task in (self._seed_task, self._task, self._cold_task):
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

    async def _run_cold_forever(self):
        while True:
            try:
                await self._cold_sweep()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("cold sweep failed")
            await asyncio.sleep(COLD_POLL_INTERVAL_SECONDS)

    async def _cold_sweep(self):
        # ponytail: covers every listed ticker so the market grid isn't empty;
        # Redis-only (no PriceHistory write) — persisting 1730 x every 5min
        # would add ~144k rows/day to Supabase.
        async with AsyncSessionLocal() as session:
            tickers = (
                await session.execute(select(Stock.ticker).where(Stock.listed == True))
            ).scalars().all()
        if not tickers:
            return
        try:
            quotes = await asyncio.to_thread(fetch_quotes_bulk, list(tickers))
        except (Exception, SystemExit) as e:
            logger.warning("bulk quote fetch failed: %s", e)
            return
        written = 0
        for ticker, data in quotes.items():
            try:
                await set_quote_with_timestamp(
                    self.redis_client, ticker, data, ttl_seconds=COLD_TTL_SECONDS
                )
                written += 1
            except Exception as e:
                logger.warning("cold redis set failed for %s: %s", ticker, e)
        logger.info("cold sweep wrote %d/%d quotes", written, len(quotes))

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
            tickers = [ticker for _, ticker in rows]
            if not tickers:
                return
            try:
                quotes = await asyncio.to_thread(fetch_quotes_bulk, tickers)
            except (Exception, SystemExit) as e:
                logger.warning("bulk quote fetch failed: %s", e)
                return
            for stock_id, ticker in rows:
                data = quotes.get(ticker)
                if not data:
                    continue
                close_price = data.get("close_price")
                if not close_price:
                    logger.warning("no close_price for %s", ticker)
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
            try:
                await session.commit()
            except Exception:
                logger.exception("price_history commit failed")
                await session.rollback()


async def main():
    """Run the poller standalone (same tasks as the API lifespan)."""
    poller = PricePoller()
    await poller.start()
    logger.info("price poller started")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        await poller.stop()
        logger.info("price poller stopped")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass