
import os, sys
sys.path.insert(0,
os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import select
from sqlalchemy.orm import Session
from vnstock.explorer.vci.listing import Listing
from vnstock.ui.market import Market

from api.database import SessionLocal
from api.models import Stock


def fetch_stocks_from_vnstock() -> list[dict]:
    df = Listing().symbols_by_industries(lang="en")
    df = df.rename(columns={
        "symbol": "ticker",
        "organ_name": "company_name",
        "icb_name": "sector",
    })
    cols = [c for c in ["ticker", "company_name", "exchange", "sector"] if c in df.columns]
    return df[cols].to_dict(orient="records")


def upsert_stocks(db: Session, rows: list[dict]) -> int:
    count = 0
    for r in rows:
        existing = db.scalar(select(Stock).where(Stock.ticker == r["ticker"]))
        if existing:
            existing.company_name = r["company_name"]
            existing.exchange = r["exchange"]
            existing.sector = r["sector"]
            if r.get("listing_date"):
                existing.listing_date = r["listing_date"]
        else:
            payload = {k: r.get(k) for k in ("company_name", "exchange", "sector", "listing_date")}
            payload["listed"] = r.get("listed", True)
            payload["ticker"] = r["ticker"]
            db.add(Stock(**payload))
        count += 1
    db.commit()
    return count


def get_market_snapshot(ticker: str) -> dict:
    df = Market().equity(ticker).quote()
    if df.empty:
        return {}
    return df.iloc[0].to_dict()


def fetch_quotes_bulk(tickers: list[str]) -> dict[str, dict]:
    """One vnstock request for all tickers -> {TICKER: quote dict}."""
    if not tickers:
        return {}
    df = Market().quote(symbol=tickers)
    if df is None or df.empty:
        return {}
    out: dict[str, dict] = {}
    for r in df.to_dict(orient="records"):
        ticker = str(r.get("symbol", "")).upper()
        if not ticker:
            continue
        out[ticker] = {k: (None if v is None or v != v else v) for k, v in r.items()}
    return out
