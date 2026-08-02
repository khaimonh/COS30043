import asyncio, logging, os
import httpx
from sqlalchemy import select
from api.database import AsyncSessionLocal, async_engine
from api.models import Stock, PriceHistory
from api.services.redis_service import get_redis

logger = logging.getLogger("price_poller")

POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "10"))
PRICE_TTL_SECONDS = int(os.getenv("PRICE_TTL_SECONDS", "15"))
PRICE_API_BASE_URL = os.getenv("PRICE_API_BASE_URL", "http://localhost:8000")
PRICE_API_TIMEOUT = float(os.getenv("PRICE_API_TIMEOUT", "10"))

QUOTE_DELAY_SECONDS = 3.1

logger = logging.getLogger("price_poller")

class PricePoller:
    def __init__(self):
        self._task: asyncio.Task | None = None
        self.redis_client=get_redis()

    async def start(self):
        self._task = asyncio.create_task(self._loop(), name="price-poller")

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def run_once(self):
        async with AsyncSessionLocal() as session:
            rows = (await session.execute(select(Stock.stock_id, Stock.ticker).where(Stock.listed == True))).all()
            for stock_id, ticker in rows:
                try:
                    async with httpx.AsyncClient(timeout=PRICE_API_TIMEOUT) as client:
                        r = await client.get(f"{PRICE_API_BASE_URL}/stocks/{ticker}/quote")
                        r.raise_for_status()
                        close_price = r.json().get("close_price")
                except (httpx.HTTPError, ValueError) as e:
                    logger.warning("quote fetch failed for %s: %s", ticker, e)
                    await asyncio.sleep(QUOTE_DELAY_SECONDS)
                    continue
                if not close_price:
                    logger.warning("no close_price for %s", ticker)
                    await asyncio.sleep(QUOTE_DELAY_SECONDS)
                    continue

                try:
                    await self.redis_client.set(f"price:{ticker}", str(close_price), ex=PRICE_TTL_SECONDS)
                except Exception as e:
                    logger.warning("redis set failed for %s: %s", ticker, e)
                session.add(PriceHistory(stock_id=stock_id, price=close_price))
                await asyncio.sleep(QUOTE_DELAY_SECONDS)
            try:
                await session.commit()
            except Exception:
                logger.exception("price_history commit failed")
                await session.rollback()