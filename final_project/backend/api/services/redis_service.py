import json
import os
import time
import redis
import redis.asyncio as aioredis

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


async def get_cached_quote(ticker: str) -> dict | None:
    try:
        cached = await get_redis().get(f"price:{ticker}")
    except Exception:
        return None
    if not cached:
        return None
    try:
        return json.loads(cached)
    except Exception:
        return None

async def get_quote_with_timestamp(redis, ticker: str) -> tuple[float | None, int | None]:
    pipe = redis.pipeline()
    pipe.get(f"price:{ticker}")
    pipe.get(f"quote_timestamp:{ticker}")
    price_raw, timestamp_raw = await pipe.execute()
    if price_raw is None:
        return None, None
    price = float(price_raw)
    timestamp_ms = int(timestamp_raw) if timestamp_raw is not None else None
    return price, timestamp_ms

async def set_quote_with_timestamp(redis, ticker: str, price: float) -> int:
    timestamp_ms = int(time.time() * 1000)
    pipe = redis.pipeline()
    pipe.set(f"price:{ticker}", price)
    pipe.set(f"quote_timestamp:{ticker}", timestamp_ms)
    await pipe.execute()
    return timestamp_ms

async def publish_quote(redis, ticker: str, price: float, timestamp_ms: int) -> None:
    payload = json.dumps({"symbol": ticker, "price": price, "timestamp": timestamp_ms})
    await redis.publish(f"quotes:{ticker}", payload)