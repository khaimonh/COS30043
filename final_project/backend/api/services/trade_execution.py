import json
import logging
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from api.database import SessionLocal
from api.models import (
    Holding,
    HoldingAllocation,
    Order,
    OrderStatus,
    OrderStyle,
    Portfolio,
    Trade,
)
from api.services.redis_service import get_redis_sync
from api.services.stock_service import get_market_snapshot

logger = logging.getLogger("trade_execution")

MAX_RETRIES = 3


def execute_order(order_id: str) -> None:
    """Execute a pending order. Called by the RabbitMQ consumer, one order at a time."""
    for attempt in range(MAX_RETRIES):
        with SessionLocal() as db:
            try:
                _execute_once(db, order_id)
                db.commit()
                logger.info("order %s processed", order_id)
                return
            except StaleDataError:
                db.rollback()
                if attempt == MAX_RETRIES - 1:
                    _reject_order(order_id, "concurrent update conflict")
                    raise
            except Exception:
                db.rollback()
                logger.exception("execution failed for order %s", order_id)
                _reject_order(order_id, "execution error")
                raise


def _execute_once(db: Session, order_id: str) -> None:
    order = db.scalar(
        select(Order).where(Order.order_id == order_id).with_for_update()
    )
    if order is None:
        return
    if order.status != OrderStatus.PENDING:
        return  # already processed — idempotent

    price = _resolve_price(db, order)
    if price is None:
        order.status = OrderStatus.REJECTED
        return

    if order.order_type.value == "Buy":
        _execute_buy(db, order, price)
    else:
        _execute_sell(db, order, price)


def _resolve_price(db: Session, order: Order) -> Decimal | None:
    quote = None
    try:
        cached = get_redis_sync().get(f"price:{order.stock.ticker}")
        if cached:
            quote = json.loads(cached).get("close_price")
    except Exception:
        quote = None

    if quote is None:
        try:
            snapshot = get_market_snapshot(order.stock.ticker)
            quote = snapshot.get("close_price") if snapshot else None
        except Exception:
            logger.exception("price fallback failed for %s", order.stock.ticker)
            quote = None

    if quote is None:
        return None
    quote = Decimal(str(quote))

    if order.order_style == OrderStyle.LIMIT and order.limit_price is not None:
        if order.order_type.value == "Buy":
            price = min(quote, order.limit_price)
        else:
            price = max(quote, order.limit_price)
    else:
        price = quote
    return price


def _execute_buy(db: Session, order: Order, price: Decimal) -> None:
    portfolio = db.scalar(
        select(Portfolio).where(
            Portfolio.portfolio_id == order.portfolio_id
        ).with_for_update()
    )

    cost = price * order.quantity
    if portfolio.cash_balance < cost:
        order.status = OrderStatus.REJECTED
        return

    portfolio.cash_balance -= cost

    holding = Holding(
        portfolio_id=portfolio.portfolio_id,
        stock_id=order.stock_id,
        purchase_price=price,
        original_quantity=order.quantity,
        remaining_quantity=order.quantity,
    )
    db.add(holding)

    db.add(Trade(
        order_id=order.order_id,
        execution_price=price,
        executed_quantity=order.quantity,
    ))

    order.status = OrderStatus.FILLED


def _execute_sell(db: Session, order: Order, price: Decimal) -> None:
    portfolio = db.scalar(
        select(Portfolio).where(
            Portfolio.portfolio_id == order.portfolio_id
        ).with_for_update()
    )

    lots = db.scalars(
        select(Holding)
        .where(
            Holding.portfolio_id == order.portfolio_id,
            Holding.stock_id == order.stock_id,
            Holding.remaining_quantity > 0,
        )
        .order_by(Holding.purchase_date.asc())
        .with_for_update()
    ).all()

    available = sum(lot.remaining_quantity for lot in lots)
    if available < order.quantity:
        order.status = OrderStatus.REJECTED
        return

    trade = Trade(
        order_id=order.order_id,
        execution_price=price,
        executed_quantity=order.quantity,
    )
    db.add(trade)
    db.flush()

    remaining_to_consume = order.quantity
    for lot in lots:
        if remaining_to_consume <= 0:
            break
        consumed = min(lot.remaining_quantity, remaining_to_consume)
        lot.remaining_quantity -= consumed
        remaining_to_consume -= consumed
        db.add(HoldingAllocation(
            trade_id=trade.trade_id,
            holding_id=lot.holding_id,
            quantity_consumed=consumed,
        ))

    portfolio.cash_balance += price * order.quantity
    order.status = OrderStatus.FILLED


def _reject_order(order_id: str, reason: str) -> None:
    with SessionLocal() as db:
        order = db.scalar(select(Order).where(Order.order_id == order_id))
        if order and order.status == OrderStatus.PENDING:
            order.status = OrderStatus.REJECTED
            db.commit()
        logger.warning("order %s rejected: %s", order_id, reason)
