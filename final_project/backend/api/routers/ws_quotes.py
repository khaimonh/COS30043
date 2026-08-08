import asyncio
import json
import time

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from api.database import AsyncSessionLocal
from api.models import Stock
from api.services.redis_service import get_redis, get_latest_history_batch

router = APIRouter(tags=["ws"])


async def _snapshot(tickers: list[str]) -> dict:
    """Redis prices for tickers; PriceHistory fallback for cold keys."""
    pipe = get_redis().pipeline()
    for t in tickers:
        pipe.get(f"price:{t}")
    raw_values = await pipe.execute()
    now_ms = int(time.time() * 1000)
    result: dict = {}
    missing: list[str] = []
    for t, raw in zip(tickers, raw_values):
        if raw is not None:
            try:
                payload = json.loads(raw)
                ts = payload.get("timestamp")
                result[t] = {**payload, "age_ms": (now_ms - ts) if ts else None}
                continue
            except (TypeError, ValueError):
                pass
        result[t] = None
        missing.append(t)
    if missing:
        async with AsyncSessionLocal() as db:
            rows = (
                await db.execute(
                    select(Stock.stock_id, Stock.ticker).where(Stock.ticker.in_(missing))
                )
            ).all()
            sid_by_ticker = {r.ticker: r.stock_id for r in rows}
            sids = [sid_by_ticker[t] for t in missing if t in sid_by_ticker]
            latest = await db.run_sync(get_latest_history_batch, sids)
            for t in missing:
                sid = sid_by_ticker.get(t)
                if sid is not None and sid in latest:
                    price, recorded_at = latest[sid]
                    ts_ms = int(recorded_at.timestamp() * 1000) if recorded_at else None
                    result[t] = {
                        "close_price": str(price),
                        "timestamp": ts_ms,
                        "age_ms": (now_ms - ts_ms) if ts_ms else None,
                        "fallback": "history",
                    }
    return result


@router.websocket("/ws/quotes")
async def ws_quotes(websocket: WebSocket):
    await websocket.accept()
    subscribed: set[str] = set()
    pubsub = get_redis().pubsub()
    await pubsub.psubscribe("quotes:*")

    async def reader():
        async for msg in pubsub.listen():
            if msg["type"] != "pmessage":
                continue
            ticker = str(msg["channel"]).split(":", 1)[1]
            if ticker not in subscribed:
                continue
            try:
                data = json.loads(msg["data"])
            except (TypeError, ValueError):
                continue
            ts = data.get("timestamp")
            age_ms = (int(time.time() * 1000) - ts) if ts else None
            try:
                await websocket.send_json({"type": "tick", "ticker": ticker, **data, "age_ms": age_ms})
            except Exception:
                return

    reader_task = asyncio.create_task(reader())
    try:
        while True:
            text = await websocket.receive_text()
            try:
                message = json.loads(text)
            except ValueError:
                continue
            op = message.get("op")
            if op == "subscribe":
                tickers = [str(t).upper() for t in message.get("tickers", [])]
                fresh = [t for t in tickers if t and t not in subscribed]
                subscribed.update(fresh)
                if fresh:
                    await websocket.send_json({"type": "snapshot", "quotes": await _snapshot(fresh)})
            elif op == "unsubscribe":
                subscribed.difference_update(
                    str(t).upper() for t in message.get("tickers", [])
                )
    except WebSocketDisconnect:
        pass
    finally:
        reader_task.cancel()
        try:
            await reader_task
        except asyncio.CancelledError:
            pass
        await pubsub.aclose()
