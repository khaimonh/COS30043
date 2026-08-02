
import os, sys
sys.path.insert(0,
os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import select
from sqlalchemy.orm import Session
from vnstock.explorer.vci.listing import Listing
from vnstock.ui.market import Market

from api.database import SessionLocal
from api.models import Stock


def fetch_stocks_from_vnstock(lang: str = "en") -> list[dict]:
    df = Listing().symbols_by_industries(lang=lang)
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


def get_all_stocks(db: Session) -> list[Stock]:
    return list(db.scalars(select(Stock)).all())


def get_stock_by_ticker(db: Session, ticker: str) -> Stock | None:
    return db.scalar(select(Stock).where(Stock.ticker == ticker))


def get_market_snapshot(ticker: str) -> dict:
    df = Market().equity(ticker).quote()
    if df.empty:
        return {}
    return df.iloc[0].to_dict()
