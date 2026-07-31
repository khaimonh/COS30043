from dotenv import load_dotenv
from pydantic import BaseModel

import pandas as pd
import io
from fastapi import APIRouter, status, HTTPException, File, UploadFile

from api.deps import db_dependency, admin_dependency

from api.services.stock_service import (
    upsert_stocks, fetch_stocks_from_vnstock, get_all_stocks, get_stock_by_ticker,
)

load_dotenv()

router = APIRouter(
    prefix='/stocks',
    tags=['stocks']
)

REQUIRED_COLS = {"ticker", "company_name", "exchange", "sector"}


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

    rows = []
    for r in df.to_dict(orient="records"):
        row = {
            "ticker": r["ticker"],
            "company_name": r["company_name"],
            "exchange": r.get("exchange", ""),
            "sector": r["sector"],
            "listed": True,
        }
        if "listing_date" in r and r["listing_date"]:
            raw_date = r["listing_date"]
            if raw_date:
                try:
                    row["listing_date"] = pd.to_datetime(raw_date).tz_localize("UTC").floor("us").to_pydatetime()
                except Exception:
                    row["listing_date"] = None
        rows.append(row)

    n = upsert_stocks(db, rows)
    return {"imported": n, "source": "csv"}


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
