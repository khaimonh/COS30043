from dotenv import load_dotenv
from pydantic import BaseModel

import json
import pandas as pd
import io
from fastapi import APIRouter, status, HTTPException, File, UploadFile, Query
from sqlalchemy import select

from api.deps import db_dependency, admin_dependency

from api.services.stock_service import (
    upsert_stocks, fetch_stocks_from_vnstock, get_market_snapshot,
)
from api.services.redis_service import get_redis
from api.models import Stock, PriceHistory

load_dotenv()

router = APIRouter(
    prefix='/stocks',
    tags=['stocks']
)

REQUIRED_COLS = {"ticker", "company_name", "exchange", "sector"}


class StockUpdateRequest(BaseModel):
    company_name: str | None = None
    exchange: str | None = None
    sector: str | None = None
    listed: bool | None = None


def _build_rows(df: pd.DataFrame) -> list[dict]:
    rows = []
    for r in df.to_dict(orient="records"):
        row = {
            "ticker": r["ticker"],
            "company_name": r["company_name"],
            "exchange": r.get("exchange", ""),
            "sector": r["sector"],
            "listed": True,
        }
        if r.get("listing_date"):
            try:
                row["listing_date"] = pd.to_datetime(r["listing_date"]).tz_localize("UTC").floor("us").to_pydatetime()
            except Exception:
                row["listing_date"] = None
        rows.append(row)
    return rows


@router.post('/import', status_code=status.HTTP_201_CREATED)
async def import_stocks(db: db_dependency, _: admin_dependency):
    rows = fetch_stocks_from_vnstock()
    n = upsert_stocks(db, rows)
    return {"imported": n}


@router.post('/import-csv', status_code=status.HTTP_201_CREATED)
async def import_stocks_csv(db: db_dependency, _: admin_dependency, file: UploadFile = File(...)):
    raw = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw), dtype=str).fillna("")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"bad csv: {e}")

    RENAME_MAP = {"symbol": "ticker", "organ_name": "company_name"}
    df = df.rename(columns=RENAME_MAP)

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise HTTPException(status_code=400, detail=f"missing columns: {sorted(missing)}")

    n = upsert_stocks(db, _build_rows(df))
    return {"imported": n, "source": "csv"}


@router.get('/quotes', status_code=status.HTTP_200_OK)
async def get_all_quotes(db: db_dependency):
    tickers = [s.ticker for s in db.scalars(select(Stock)).all()]
    if not tickers:
        return {}
    try:
        cached = await get_redis().mget(*[f"price:{t}" for t in tickers])
    except Exception:
        cached = [None] * len(tickers)
    result = {}
    for ticker, raw in zip(tickers, cached):
        result[ticker] = json.loads(raw) if raw else None
    return result


@router.get('/{ticker}/quote', status_code=status.HTTP_200_OK)
async def get_quote(ticker: str):
    try:
        cached = await get_redis().get(f"price:{ticker}")
    except Exception:
        cached = None
    if cached:
        return json.loads(cached)
    q = get_market_snapshot(ticker)
    if not q:
        raise HTTPException(status_code=404, detail=f"ticker '{ticker}' not found")
    return q


@router.get('/{ticker}/history', status_code=status.HTTP_200_OK)
async def get_price_history(
    ticker: str,
    db: db_dependency,
    limit: int = Query(100, ge=1, le=500),
):
    stock = db.scalar(select(Stock).where(Stock.ticker == ticker))
    if stock is None:
        raise HTTPException(status_code=404, detail=f"ticker '{ticker}' not found")
    rows = db.scalars(
        select(PriceHistory)
        .where(PriceHistory.stock_id == stock.stock_id)
        .order_by(PriceHistory.recorded_at.desc())
        .limit(limit)
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
async def get_stock(ticker: str, db: db_dependency):
    s = db.scalar(select(Stock).where(Stock.ticker == ticker))
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
async def update_stock(ticker: str, payload: StockUpdateRequest, db: db_dependency, _: admin_dependency):
    s = db.scalar(select(Stock).where(Stock.ticker == ticker))
    if s is None:
        raise HTTPException(status_code=404, detail=f"ticker '{ticker}' not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(s, field, value)
    db.commit()
    return {"detail": f"Stock '{ticker}' updated"}


@router.delete('/{ticker}', status_code=status.HTTP_200_OK)
async def delist_stock(ticker: str, db: db_dependency, _: admin_dependency):
    s = db.scalar(select(Stock).where(Stock.ticker == ticker))
    if s is None:
        raise HTTPException(status_code=404, detail=f"ticker '{ticker}' not found")
    s.listed = False
    db.commit()
    return {"detail": f"Stock '{ticker}' delisted"}


@router.get('/', status_code=status.HTTP_200_OK)
async def get_stocks(db: db_dependency):
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
        for s in db.scalars(select(Stock)).all()
    ]
