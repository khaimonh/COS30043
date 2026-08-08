import json
import os
import time
import redis
import redis.asyncio as aioredis
from sqlalchemy import select

from api.models import PriceHistory

PRICE_TTL_SECONDS = int(os.getenv("PRICE_TTL_SECONDS", "15"))

_client: aioredis.Redis | None = None
_sync_client: redis.Redis | None = None


def get_redis() -> aioredis.Redis:
    global _client
    if _client is None:
        _client = aioredis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            decode_responses=True,
        )
    return _client


def get_redis_sync() -> redis.Redis:
    global _sync_client
    if _sync_client is None:
        _sync_client = redis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            decode_responses=True,
        )
    return _sync_client


async def get_cached_quote(ticker: str, db=None, stock_id=None) -> dict | None:
    """Read the cached quote JSON, falling back to the latest PriceHistory row.

    db must be a sync Session and stock_id must be given for the fallback.
    The fallback return includes a real `timestamp` (the record's recorded_at)
    so callers can judge freshness.
    """
    try:
        cached = await get_redis().get(f"price:{ticker}")
    except Exception:
        cached = None
    if cached:
        try:
            return json.loads(cached)
        except Exception:
            pass
    if db is None or stock_id is None:
        return None
    price, recorded_at = get_latest_history(db, stock_id)
    if price is None:
        return None
    ts_ms = int(recorded_at.timestamp() * 1000) if recorded_at else None
    return {"close_price": str(price), "timestamp": ts_ms}


def get_latest_history(db, stock_id) -> tuple[object | None, object | None]:
    """Latest (price, recorded_at) from PriceHistory for a stock, or (None, None).

    price/recorded_at are returned as-is (Decimal / datetime). Callers convert.
    """
    row = db.execute(
        select(PriceHistory.price, PriceHistory.recorded_at)
        .where(PriceHistory.stock_id == stock_id)
        .order_by(PriceHistory.recorded_at.desc())
        .limit(1)
    ).first()
    if row is None:
        return None, None
    return row.price, row.recorded_at


def get_latest_history_batch(db, stock_ids) -> dict:
    """stock_id -> (price, recorded_at) for the latest row per stock."""
    if not stock_ids:
        return {}
    rows = db.execute(
        select(PriceHistory.stock_id, PriceHistory.price, PriceHistory.recorded_at)
        .where(PriceHistory.stock_id.in_(stock_ids))
        .order_by(PriceHistory.recorded_at.desc())
    ).all()
    latest = {}
    for row in rows:
        if row.stock_id not in latest:
            latest[row.stock_id] = (row.price, row.recorded_at)
    return latest

async def get_quote_with_timestamp(redis, ticker: str) -> tuple[dict | None, int | None]:
    """Read the cached quote JSON and the write timestamp.

    Returns (payload, timestamp_ms). Both are None on a true cache miss.
    payload is the parsed JSON dict written by the price poller.
    timestamp_ms is epoch milliseconds, or None if the poller hasn't
    written a timestamp key yet (e.g. before set_quote_with_timestamp
    is wired up).
    """
    pipe = redis.pipeline()
    pipe.get(f"price:{ticker}")
    pipe.get(f"quote_timestamp:{ticker}")
    price_raw, timestamp_raw = await pipe.execute()
    if price_raw is None:
        return None, None
    try:
        payload = json.loads(price_raw)
    except (TypeError, ValueError):
        return None, None
    timestamp_ms = int(timestamp_raw) if timestamp_raw is not None else None
    return payload, timestamp_ms

async def set_quote_with_timestamp(redis, ticker: str, payload: dict, ts_ms: int | None = None) -> int:
    timestamp_ms = ts_ms if ts_ms is not None else int(time.time() * 1000)
    payload = {**payload, "timestamp": timestamp_ms}
    pipe = redis.pipeline()
    pipe.set(f"price:{ticker}", json.dumps(payload), ex=PRICE_TTL_SECONDS)
    pipe.set(f"quote_timestamp:{ticker}", timestamp_ms)
    await pipe.execute()
    return timestamp_ms


async def publish_quote(redis, ticker: str, payload: dict, timestamp_ms: int) -> None:
    await redis.publish(f"quotes:{ticker}", json.dumps({**payload, "timestamp": timestamp_ms}))