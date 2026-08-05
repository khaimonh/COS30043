from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from sqlalchemy import select, func

from api.deps import db_dependency, admin_dependency
from api.models import User, Role, UserStatus, Order, OrderStatus, Trade, Stock
from api.services.queue import ORDER_QUEUE_NAME, ORDER_DLQ_NAME, _connect

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


class UserStatusUpdateRequest(BaseModel):
    status: UserStatus


@router.get('/users', status_code=status.HTTP_200_OK)
async def list_users(db: db_dependency, _: admin_dependency):
    users = db.scalars(
        select(User).join(Role).order_by(User.created_at)
    ).all()
    return [
        {
            "user_id": str(u.user_id),
            "email": u.email,
            "full_name": f"{u.first_name} {u.last_name}",
            "role": u.role.role_name,
            "status": u.status.value,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]


@router.patch('/users/{user_id}/status', status_code=status.HTTP_200_OK)
async def update_user_status(
    user_id: str,
    update_request: UserStatusUpdateRequest,
    db: db_dependency,
    _: admin_dependency,
):
    user = db.scalar(select(User).where(User.user_id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = update_request.status
    db.commit()
    return {"user_id": str(user.user_id), "status": user.status.value}


@router.get('/orders', status_code=status.HTTP_200_OK)
async def list_all_orders(db: db_dependency, _: admin_dependency):
    orders = db.scalars(
        select(Order).order_by(Order.created_at.desc())
    ).all()
    return [
        {
            "order_id": str(o.order_id),
            "user_email": o.user.email,
            "ticker": o.stock.ticker,
            "portfolio_id": str(o.portfolio_id),
            "order_type": o.order_type.value,
            "order_style": o.order_style.value,
            "status": o.status.value,
            "quantity": o.quantity,
            "limit_price": str(o.limit_price) if o.limit_price else None,
            "created_at": o.created_at.isoformat() if o.created_at else None,
        }
        for o in orders
    ]


@router.get('/trades', status_code=status.HTTP_200_OK)
async def list_all_trades(db: db_dependency, _: admin_dependency):
    trades = db.scalars(
        select(Trade).order_by(Trade.executed_at.desc())
    ).all()
    return [
        {
            "trade_id": str(t.trade_id),
            "order_id": str(t.order_id),
            "user_email": t.order.user.email,
            "ticker": t.order.stock.ticker,
            "execution_price": str(t.execution_price),
            "executed_quantity": t.executed_quantity,
            "executed_at": t.executed_at.isoformat() if t.executed_at else None,
        }
        for t in trades
    ]


@router.get('/health', status_code=status.HTTP_200_OK)
async def system_health(db: db_dependency, _: admin_dependency):
    counts = dict(
        db.execute(
            select(Order.status, func.count()).group_by(Order.status)
        ).all()
    )

    queue = {"status": "up", "queue_depth": None, "dlq_depth": None}
    try:
        connection = _connect()
        try:
            channel = connection.channel()
            queue["queue_depth"] = channel.queue_declare(
                queue=ORDER_QUEUE_NAME, passive=True
            ).method.message_count
            queue["dlq_depth"] = channel.queue_declare(
                queue=ORDER_DLQ_NAME, passive=True
            ).method.message_count
        finally:
            connection.close()
    except Exception:
        queue["status"] = "unreachable"

    return {
        "queues": queue,
        "order_counts": {
            s.value: counts.get(s, 0) for s in OrderStatus
        },
    }
