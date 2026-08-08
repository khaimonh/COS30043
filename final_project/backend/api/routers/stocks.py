from dotenv import load_dotenv
from pydantic import BaseModel

import json
import time
from fastapi import APIRouter, status, HTTPException, Query
from sqlalchemy import select

from api.deps import db_dependency_async, admin_dependency

from api.services.stock_service import (
    upsert_stocks, fetch_stocks_from_vnstock,
)
from api.services.redis_service import get_redis, get_latest_history, get_latest_history_batch
from api.models import Stock, PriceHistory

load_dotenv()

router = APIRouter(
    prefix='/stocks',
    tags=['stocks']
)


class StockUpdateRequest(BaseModel):
    company_name: str | None = None
    exchange: str | None = None
    sector: str | None = None
    listed: bool | None = None


@router.post('/import', status_code=status.HTTP_201_CREATED)
async def import_stocks(db: db_dependency_async, _: admin_dependency):
    rows = fetch_stocks_from_vnstock()
    n = await db.run_sync(upsert_stocks, rows)
    return {"imported": n}


@router.get('/quotes', status_code=status.HTTP_200_OK)
async def get_all_quotes(db: db_dependency_async):
    stocks = (await db.execute(select(Stock.ticker, Stock.stock_id))).all()
    if not stocks:
        return {}
    redis = get_redis()
    try:
        pipe = redis.pipeline()
        for ticker, _ in stocks:
            pipe.get(f"price:{ticker}")
        raw_values = await pipe.execute()
    except Exception:
        raw_values = [None] * len(stocks)
    result = {}
    missing = []
    for (ticker, stock_id), raw in zip(stocks, raw_values):
        if raw is not None:
            try:
                payload = json.loads(raw)
                timestamp = payload.get("timestamp")
                age_ms = (int(time.time() * 1000) - timestamp) if timestamp else None
                result[ticker] = {**payload, "age_ms": age_ms}
                continue
            except (TypeError, ValueError):
                pass
        missing.append(stock_id)
        result[ticker] = None
    if missing:
        latest = await db.run_sync(get_latest_history_batch, missing)
        for (ticker, stock_id), raw in zip(stocks, raw_values):
            if result[ticker] is None and stock_id in latest:
                price, recorded_at = latest[stock_id]
                timestamp_ms = int(recorded_at.timestamp() * 1000) if recorded_at else None
                age_ms = (int(time.time() * 1000) - timestamp_ms) if timestamp_ms else None
                result[ticker] = {
                    "close_price": str(price),
                    "timestamp": timestamp_ms,
                    "age_ms": age_ms,
                    "fallback": "history",
                }
    return result


@router.get('/{ticker}/quote', status_code=status.HTTP_200_OK)
async def get_quote(ticker: str, db: db_dependency_async):
    try:
        cached = await get_redis().get(f"price:{ticker}")
    except Exception:
        cached = None
    if cached:
        try:
            payload = json.loads(cached)
        except (TypeError, ValueError):
            payload = None
        if payload:
            timestamp = payload.get("timestamp")
            age_ms = (int(time.time() * 1000) - timestamp) if timestamp else None
            return {**payload, "age_ms": age_ms}
    stock_id = await db.scalar(select(Stock.stock_id).where(Stock.ticker == ticker))
    if stock_id is None:
        return None
    price, recorded_at = await db.run_sync(get_latest_history, stock_id)
    if price is None:
        return None
    timestamp_ms = int(recorded_at.timestamp() * 1000) if recorded_at else None
    age_ms = (int(time.time() * 1000) - timestamp_ms) if timestamp_ms else None
    return {
        "close_price": str(price),
        "timestamp": timestamp_ms,
        "age_ms": age_ms,
        "fallback": "history",
    }


@router.get('/{ticker}/history', status_code=status.HTTP_200_OK)
async def get_price_history(
    ticker: str,
    db: db_dependency_async,
    limit: int = Query(100, ge=1, le=500),
):
    stock = await db.scalar(select(Stock).where(Stock.ticker == ticker))
    if stock is None:
        raise HTTPException(status_code=404, detail=f"ticker '{ticker}' not found")
    rows = (
        await db.scalars(
            select(PriceHistory)
            .where(PriceHistory.stock_id == stock.stock_id)
            .order_by(PriceHistory.recorded_at.desc())
            .limit(limit)
        )
    ).all()
    points = []
    for r in reversed(rows):
        points.append({
            "time": r.recorded_at.isoformat() if r.recorded_at else None,
            "open": str(r.open_price) if r.open_price is not None else None,
            "high": str(r.high_price) if r.high_price is not None else None,
            "low": str(r.low_price) if r.low_price is not None else None,
            "close": str(r.price) if r.price is not None else None,
            "volume": r.volume,
        })
    return {"ticker": ticker, "points": points}


@router.get('/{ticker}', status_code=status.HTTP_200_OK)
async def get_stock(ticker: str, db: db_dependency_async):
    s = await db.scalar(select(Stock).where(Stock.ticker == ticker))
    if s is None:
        raise HTTPException(status_code=404, detail=f"ticker '{ticker}' not found")
    return {
        "stock_id": str(s.stock_id),
        "ticker": s.ticker,
        "company_name": s.company_name,
        "exchange": s.exchange,
        "sector": s.sector,
        "listing_date": s.listing_date.isoformat() if s.listing_date else None,
        "listed": s.listed,
    }


@router.put('/{ticker}', status_code=status.HTTP_200_OK)
async def update_stock(ticker: str, payload: StockUpdateRequest, db: db_dependency_async, _: admin_dependency):
    s = await db.scalar(select(Stock).where(Stock.ticker == ticker))
    if s is None:
        raise HTTPException(status_code=404, detail=f"ticker '{ticker}' not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(s, field, value)
    await db.commit()
    return {"detail": f"Stock '{ticker}' updated"}


@router.delete('/{ticker}', status_code=status.HTTP_200_OK)
async def delist_stock(ticker: str, db: db_dependency_async, _: admin_dependency):
    s = await db.scalar(select(Stock).where(Stock.ticker == ticker))
    if s is None:
        raise HTTPException(status_code=404, detail=f"ticker '{ticker}' not found")
    s.listed = False
    await db.commit()
    return {"detail": f"Stock '{ticker}' delisted"}


@router.get('/', status_code=status.HTTP_200_OK)
async def get_stocks(db: db_dependency_async):
    return [
        {
            "stock_id": str(s.stock_id),
            "ticker": s.ticker,
            "company_name": s.company_name,
            "exchange": s.exchange,
            "sector": s.sector,
            "listing_date": s.listing_date.isoformat() if s.listing_date else None,
            "listed": s.listed,
        }
        for s in (await db.scalars(select(Stock))).all()
    ]
