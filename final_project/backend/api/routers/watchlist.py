import json
from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from sqlalchemy import select

from api.deps import db_dependency, user_dependency
from api.models import Watchlist, Stock
from api.services.stock_service import get_stock_by_ticker
from api.services.redis_service import get_redis

router = APIRouter(
    prefix='/watchlist',
    tags=['watchlist']
)


class WatchlistAddRequest(BaseModel):
    ticker: str = Field(min_length=1, max_length=10)
    target_price: Decimal | None = Field(default=None, ge=0)


class WatchlistUpdateRequest(BaseModel):
    target_price: Decimal | None = None


def _get_owned_entry(db, current_user, watchlist_id: str) -> Watchlist:
    entry = db.scalar(
        select(Watchlist).where(
            Watchlist.watchlist_id == watchlist_id,
            Watchlist.user_id == current_user.user_id,
        )
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Watchlist entry not found")
    return entry


@router.get('/', status_code=status.HTTP_200_OK)
async def get_watchlist(db: db_dependency, current_user: user_dependency):
    entries = db.scalars(
        select(Watchlist).where(Watchlist.user_id == current_user.user_id)
    ).all()
    redis = get_redis()
    result = []
    for entry in entries:
        current_price = None
        try:
            cached = await redis.get(f"price:{entry.stock.ticker}")
            if cached:
                current_price = json.loads(cached).get("close_price")
        except Exception:
            current_price = None
        result.append({
            "watchlist_id": str(entry.watchlist_id),
            "stock_id": str(entry.stock.stock_id),
            "ticker": entry.stock.ticker,
            "company_name": entry.stock.company_name,
            "exchange": entry.stock.exchange,
            "sector": entry.stock.sector,
            "target_price": str(entry.target_price) if entry.target_price is not None else None,
            "current_price": str(current_price) if current_price is not None else None,
            "created_at": entry.created_at.isoformat() if entry.created_at else None,
        })
    return result


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(
    add_request: WatchlistAddRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    stock = get_stock_by_ticker(db, add_request.ticker)
    if stock is None or not stock.listed:
        raise HTTPException(status_code=404, detail=f"ticker '{add_request.ticker}' not found")

    existing = db.scalar(
        select(Watchlist).where(
            Watchlist.user_id == current_user.user_id,
            Watchlist.stock_id == stock.stock_id,
        )
    )
    if existing:
        raise HTTPException(status_code=400, detail="Stock already in watchlist")

    entry = Watchlist(
        user_id=current_user.user_id,
        stock_id=stock.stock_id,
        target_price=add_request.target_price,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {
        "watchlist_id": str(entry.watchlist_id),
        "ticker": stock.ticker,
        "target_price": str(entry.target_price) if entry.target_price is not None else None,
    }


@router.patch('/{watchlist_id}', status_code=status.HTTP_200_OK)
async def update_watchlist_entry(
    watchlist_id: str,
    update_request: WatchlistUpdateRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    entry = _get_owned_entry(db, current_user, watchlist_id)
    entry.target_price = update_request.target_price
    db.commit()
    return {
        "watchlist_id": str(entry.watchlist_id),
        "ticker": entry.stock.ticker,
        "target_price": str(entry.target_price) if entry.target_price is not None else None,
    }


@router.delete('/{watchlist_id}', status_code=status.HTTP_200_OK)
async def remove_from_watchlist(
    watchlist_id: str,
    db: db_dependency,
    current_user: user_dependency,
):
    entry = _get_owned_entry(db, current_user, watchlist_id)
    db.delete(entry)
    db.commit()
    return {"detail": "Watchlist entry removed"}
