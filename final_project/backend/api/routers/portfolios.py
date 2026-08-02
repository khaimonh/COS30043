from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from sqlalchemy import select, func

from api.deps import db_dependency, user_dependency
from api.models import Portfolio, BankAccount, CashTransaction, CashTransactionType

router = APIRouter(
    prefix='/portfolios',
    tags=['portfolios']
)

MAX_PORTFOLIOS_PER_USER = 3


class PortfolioCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class CashRequest(BaseModel):
    portfolio_id: str
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

    duplicate = db.scalar(
        select(Portfolio).where(
            Portfolio.user_id == current_user.user_id,
            Portfolio.name == create_request.name,
        )
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio name already exists",
        )

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
    portfolio = db.scalar(
        select(Portfolio).where(
            Portfolio.portfolio_id == portfolio_id,
            Portfolio.user_id == current_user.user_id,
        )
    )
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return {
        "portfolio_id": str(portfolio.portfolio_id),
        "name": portfolio.name,
        "cash_balance": str(portfolio.cash_balance),
    }


@router.put('/{portfolio_id}', status_code=status.HTTP_200_OK)
async def rename_portfolio(
    portfolio_id: str,
    create_request: PortfolioCreateRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    portfolio = _get_owned_portfolio(db, current_user, portfolio_id)

    duplicate = db.scalar(
        select(Portfolio).where(
            Portfolio.user_id == current_user.user_id,
            Portfolio.name == create_request.name,
            Portfolio.portfolio_id != portfolio_id,
        )
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio name already exists",
        )

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
    portfolio = db.scalar(
        select(Portfolio).where(
            Portfolio.portfolio_id == portfolio_id,
            Portfolio.user_id == current_user.user_id,
        )
    )
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
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
async def deposit(cash_request: CashRequest, db: db_dependency, current_user: user_dependency):
    portfolio = _get_owned_portfolio(db, current_user, cash_request.portfolio_id)
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
async def withdraw(cash_request: CashRequest, db: db_dependency, current_user: user_dependency):
    portfolio = _get_owned_portfolio(db, current_user, cash_request.portfolio_id)
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
