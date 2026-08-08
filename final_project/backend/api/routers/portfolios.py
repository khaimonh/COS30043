from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from sqlalchemy import select, func

from api.deps import db_dependency, user_dependency
from api.models import (
    Portfolio,
    BankAccount,
    CashTransaction,
    CashTransactionType,
    Holding,
    HoldingAllocation,
    Trade,
    Order,
)
from api.services.redis_service import get_cached_quote

router = APIRouter(
    prefix='/portfolios',
    tags=['portfolios']
)

MAX_PORTFOLIOS_PER_USER = 3


class PortfolioCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class CashRequest(BaseModel):
    bank_account_id: str | None = None
    amount: Decimal = Field(gt=0)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    create_request: PortfolioCreateRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    count = db.scalar(
        select(func.count()).select_from(Portfolio).where(Portfolio.user_id == current_user.user_id)
    )
    if count >= MAX_PORTFOLIOS_PER_USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {MAX_PORTFOLIOS_PER_USER} portfolios per user",
        )

    _check_duplicate_name(db, current_user, create_request.name)

    portfolio = Portfolio(user_id=current_user.user_id, name=create_request.name)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.get('/')
async def get_portfolios(db: db_dependency, current_user: user_dependency):
    portfolios = db.scalars(
        select(Portfolio).where(Portfolio.user_id == current_user.user_id)
    ).all()
    return [
        {
            "portfolio_id": str(p.portfolio_id),
            "name": p.name,
            "cash_balance": str(p.cash_balance),
        }
        for p in portfolios
    ]


@router.get('/{portfolio_id}')
async def get_portfolio(portfolio_id: str, db: db_dependency, current_user: user_dependency):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)
    return {
        "portfolio_id": str(portfolio.portfolio_id),
        "name": portfolio.name,
        "cash_balance": str(portfolio.cash_balance),
    }


@router.get('/{portfolio_id}/holdings')
async def get_holdings(portfolio_id: str, db: db_dependency, current_user: user_dependency):
    _get_owned_portfolio(db, current_user, portfolio_id)
    lots = db.scalars(
        select(Holding)
        .where(Holding.portfolio_id == portfolio_id, Holding.remaining_quantity > 0)
        .order_by(Holding.purchase_date)
    ).all()

    by_stock: dict[str, dict] = {}
    for lot in lots:
        row = by_stock.setdefault(str(lot.stock_id), {
            "ticker": lot.stock.ticker,
            "company_name": lot.stock.company_name,
            "quantity": 0,
            "avg_cost": Decimal(0),
            "lots": 0,
        })
        row["quantity"] += lot.remaining_quantity
        row["avg_cost"] = (
            row["avg_cost"] * (row["quantity"] - lot.remaining_quantity)
            + lot.purchase_price * lot.remaining_quantity
        ) / row["quantity"]
        row["lots"] += 1

    holdings = []
    for stock_id, row in by_stock.items():
        quote = await get_cached_quote(row["ticker"], db, stock_id)
        close = quote.get("close_price") if quote else None
        current_price = Decimal(str(close)) if close else None
        market_value = current_price * row["quantity"] if current_price is not None else None
        cost_basis = row["avg_cost"] * row["quantity"]
        holdings.append({
            "stock_id": stock_id,
            "ticker": row["ticker"],
            "company_name": row["company_name"],
            "quantity": row["quantity"],
            "lots": row["lots"],
            "avg_cost": str(row["avg_cost"]),
            "current_price": str(current_price) if current_price is not None else None,
            "market_value": str(market_value) if market_value is not None else None,
            "cost_basis": str(cost_basis),
            "unrealized_pnl": str(market_value - cost_basis) if market_value is not None else None,
        })
    return holdings


@router.get('/{portfolio_id}/summary')
async def get_portfolio_summary(
    portfolio_id: str, db: db_dependency, current_user: user_dependency
):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)

    cash_balance = portfolio.cash_balance

    lots = db.scalars(
        select(Holding)
        .where(Holding.portfolio_id == portfolio_id, Holding.remaining_quantity > 0)
    ).all()
    holdings_value = Decimal(0)
    per_stock = {}
    for lot in lots:
        cached = await get_cached_quote(lot.stock.ticker, db, lot.stock.stock_id)
        close = cached.get("close_price") if cached else None
        price = Decimal(str(close)) if close else None
        value = price * lot.remaining_quantity if price is not None else Decimal(0)
        row = per_stock.setdefault(str(lot.stock_id), {
            "ticker": lot.stock.ticker,
            "quantity": 0,
            "value": Decimal(0),
            "priced": price is not None,
        })
        row["quantity"] += lot.remaining_quantity
        row["value"] += value
        holdings_value += value

    total_value = cash_balance + holdings_value

    realized = db.scalars(
        select(HoldingAllocation)
        .join(Trade, Trade.trade_id == HoldingAllocation.trade_id)
        .join(Order, Order.order_id == Trade.order_id)
        .where(Order.portfolio_id == portfolio_id)
    ).all()
    realized_pnl = Decimal(0)
    for alloc in realized:
        realized_pnl += (alloc.trade.execution_price - alloc.holding.purchase_price) * alloc.quantity_consumed

    return {
        "portfolio_id": str(portfolio.portfolio_id),
        "name": portfolio.name,
        "cash_balance": str(cash_balance),
        "holdings_value": str(holdings_value),
        "total_value": str(total_value),
        "realized_pnl": str(realized_pnl),
        "allocations": [
            {
                "ticker": r["ticker"],
                "quantity": r["quantity"],
                "value": str(r["value"]),
                "weight_pct": round(r["value"] / total_value * 100, 2) if total_value else 0,
                "priced": r["priced"],
            }
            for r in per_stock.values()
        ],
    }


@router.get('/{portfolio_id}/activity')
async def get_activity(portfolio_id: str, db: db_dependency, current_user: user_dependency):
    _get_owned_portfolio(db, current_user, portfolio_id)

    cash = db.scalars(
        select(CashTransaction)
        .where(CashTransaction.portfolio_id == portfolio_id)
        .order_by(CashTransaction.created_at)
    ).all()
    trades = db.scalars(
        select(Trade).join(Order).where(Order.portfolio_id == portfolio_id)
        .order_by(Trade.executed_at)
    ).all()

    events = []
    for t in cash:
        events.append({
            "type": t.type.value,
            "amount": str(t.amount),
            "ticker": None,
            "quantity": None,
            "price": None,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        })
    for tr in trades:
        events.append({
            "type": tr.order.order_type.value,
            "amount": str(tr.execution_price * tr.executed_quantity),
            "ticker": tr.order.stock.ticker,
            "quantity": tr.executed_quantity,
            "price": str(tr.execution_price),
            "created_at": tr.executed_at.isoformat() if tr.executed_at else None,
        })
    events.sort(key=lambda e: e["created_at"], reverse=True)
    return events


@router.put('/{portfolio_id}', status_code=status.HTTP_200_OK)
async def rename_portfolio(
    portfolio_id: str,
    create_request: PortfolioCreateRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)

    _check_duplicate_name(db, current_user, create_request.name, exclude_id=portfolio_id)

    portfolio.name = create_request.name
    db.commit()
    return {"portfolio_id": str(portfolio.portfolio_id), "name": portfolio.name}


@router.delete('/{portfolio_id}', status_code=status.HTTP_200_OK)
async def delete_portfolio(portfolio_id: str, db: db_dependency, current_user: user_dependency):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)
    db.delete(portfolio)
    db.commit()
    return {"detail": "Portfolio deleted"}


@router.get('/{portfolio_id}/transactions')
async def get_transactions(portfolio_id: str, db: db_dependency, current_user: user_dependency):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)
    transactions = db.scalars(
        select(CashTransaction)
        .where(CashTransaction.portfolio_id == portfolio_id)
        .order_by(CashTransaction.created_at.desc())
    ).all()
    return [
        {
            "transaction_id": str(t.transaction_id),
            "type": t.type.value,
            "amount": str(t.amount),
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in transactions
    ]


@router.post('/{portfolio_id}/deposit', status_code=status.HTTP_200_OK)
async def deposit(
    portfolio_id: str,
    cash_request: CashRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)
    _check_bank_account(db, current_user, cash_request.bank_account_id)

    portfolio.cash_balance += cash_request.amount
    db.add(CashTransaction(
        portfolio_id=portfolio.portfolio_id,
        bank_account_id=cash_request.bank_account_id,
        type=CashTransactionType.DEPOSIT,
        amount=cash_request.amount,
    ))
    db.commit()
    return {"cash_balance": str(portfolio.cash_balance)}


@router.post('/{portfolio_id}/withdraw', status_code=status.HTTP_200_OK)
async def withdraw(
    portfolio_id: str,
    cash_request: CashRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)
    _check_bank_account(db, current_user, cash_request.bank_account_id)

    if portfolio.cash_balance < cash_request.amount:
        raise HTTPException(status_code=400, detail="Insufficient cash balance")

    portfolio.cash_balance -= cash_request.amount
    db.add(CashTransaction(
        portfolio_id=portfolio.portfolio_id,
        bank_account_id=cash_request.bank_account_id,
        type=CashTransactionType.WITHDRAWAL,
        amount=cash_request.amount,
    ))
    db.commit()
    return {"cash_balance": str(portfolio.cash_balance)}


@router.delete('/{portfolio_id}/transactions/{transaction_id}', status_code=status.HTTP_200_OK)
async def delete_transaction(
    portfolio_id: str,
    transaction_id: str,
    db: db_dependency,
    current_user: user_dependency,
):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)
    transaction = db.scalar(
        select(CashTransaction).where(
            CashTransaction.transaction_id == transaction_id,
            CashTransaction.portfolio_id == portfolio_id,
        )
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if transaction.type == CashTransactionType.DEPOSIT:
        portfolio.cash_balance -= transaction.amount
    else:
        portfolio.cash_balance += transaction.amount

    db.delete(transaction)
    db.commit()
    return {"cash_balance": str(portfolio.cash_balance)}


def _check_duplicate_name(db, current_user, name: str, exclude_id: str | None = None) -> None:
    q = select(Portfolio).where(
        Portfolio.user_id == current_user.user_id,
        Portfolio.name == name,
    )
    if exclude_id is not None:
        q = q.where(Portfolio.portfolio_id != exclude_id)
    if db.scalar(q) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio name already exists",
        )


def _get_owned_portfolio(db, current_user, portfolio_id: str) -> Portfolio:
    portfolio = db.scalar(
        select(Portfolio).where(
            Portfolio.portfolio_id == portfolio_id,
            Portfolio.user_id == current_user.user_id,
        )
    )
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


def _check_bank_account(db, current_user, bank_account_id: str | None):
    if bank_account_id is None:
        return
    ba = db.scalar(
        select(BankAccount).where(
            BankAccount.bank_account_id == bank_account_id,
            BankAccount.user_id == current_user.user_id,
        )
    )
    if not ba:
        raise HTTPException(status_code=404, detail="Bank account not found")
