from dotenv import load_dotenv
from pydantic import BaseModel

import json
import pandas as pd
import io
from fastapi import APIRouter, status, HTTPException, File, UploadFile

from api.deps import db_dependency, admin_dependency

from api.services.stock_service import (
    upsert_stocks, fetch_stocks_from_vnstock, get_all_stocks, get_stock_by_ticker,
    get_market_snapshot,
)
from api.services.redis_service import get_redis

load_dotenv()

router = APIRouter(
    prefix='/stocks',
    tags=['stocks']
)

REQUIRED_COLS = {"ticker", "company_name", "exchange", "sector"}


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


@router.get('/{ticker}', status_code=status.HTTP_200_OK)
async def get_stock(ticker: str, db: db_dependency):
    s = get_stock_by_ticker(db, ticker)
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
        for s in get_all_stocks(db)
    ]
