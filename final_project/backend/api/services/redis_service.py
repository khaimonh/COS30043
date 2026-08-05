import json
import os
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