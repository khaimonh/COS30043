from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from sqlalchemy import select

from api.deps import db_dependency, user_dependency
from api.models import (
    Order,
    OrderStatus,
    OrderStyle,
    OrderType,
    Portfolio,
    Stock,
)
from api.services.order_queue import publish_order

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


class OrderCreateRequest(BaseModel):
    portfolio_id: str
    stock_ticker: str
    order_type: OrderType
    order_style: OrderStyle
    quantity: int = Field(gt=0)
    limit_price: Decimal | None = Field(default=None, ge=0)


@router.post('/', status_code=status.HTTP_202_ACCEPTED)
async def create_order(
    create_request: OrderCreateRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    if create_request.order_style == OrderStyle.LIMIT and create_request.limit_price is None:
        raise HTTPException(status_code=400, detail="limit_price required for limit orders")

    portfolio = db.scalar(
        select(Portfolio).where(
            Portfolio.portfolio_id == create_request.portfolio_id,
            Portfolio.user_id == current_user.user_id,
        )
    )
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    stock = db.scalar(select(Stock).where(Stock.ticker == create_request.stock_ticker))
    if not stock or not stock.listed:
        raise HTTPException(status_code=404, detail="Stock not found or delisted")

    order = Order(
        user_id=current_user.user_id,
        portfolio_id=portfolio.portfolio_id,
        stock_id=stock.stock_id,
        order_type=create_request.order_type,
        order_style=create_request.order_style,
        status=OrderStatus.PENDING,
        quantity=create_request.quantity,
        limit_price=create_request.limit_price,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    publish_order(str(order.order_id))

    return {"order_id": str(order.order_id), "status": order.status.value}


@router.get('/')
async def get_orders(db: db_dependency, current_user: user_dependency):
    orders = db.scalars(
        select(Order).where(Order.user_id == current_user.user_id)
    ).all()
    return [
        {
            "order_id": str(o.order_id),
            "portfolio_id": str(o.portfolio_id),
            "stock_id": str(o.stock_id),
            "order_type": o.order_type.value,
            "order_style": o.order_style.value,
            "status": o.status.value,
            "quantity": o.quantity,
            "limit_price": str(o.limit_price) if o.limit_price else None,
            "created_at": o.created_at.isoformat() if o.created_at else None,
        }
        for o in orders
    ]


@router.get('/{order_id}')
async def get_order(order_id: str, db: db_dependency, current_user: user_dependency):
    order = db.scalar(
        select(Order).where(
            Order.order_id == order_id,
            Order.user_id == current_user.user_id,
        )
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "order_id": str(order.order_id),
        "portfolio_id": str(order.portfolio_id),
        "stock_id": str(order.stock_id),
        "order_type": order.order_type.value,
        "order_style": order.order_style.value,
        "status": order.status.value,
        "quantity": order.quantity,
        "limit_price": str(order.limit_price) if order.limit_price else None,
        "created_at": order.created_at.isoformat() if order.created_at else None,
    }
