from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from sqlalchemy import select

from api.deps import db_dependency, user_dependency
from api.models import BankAccount

router = APIRouter(
    prefix='/bank-accounts',
    tags=['bank-accounts']
)


class BankAccountCreateRequest(BaseModel):
    bank_name: str = Field(min_length=1, max_length=255)
    account_number: str = Field(min_length=6, max_length=34)


def _mask(account_number: str) -> str:
    return "*" * max(len(account_number) - 4, 0) + account_number[-4:]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_bank_account(
    create_request: BankAccountCreateRequest,
    db: db_dependency,
    current_user: user_dependency,
):
    account = BankAccount(
        user_id=current_user.user_id,
        bank_name=create_request.bank_name,
        account_number_encrypted=create_request.account_number,
        account_number_masked=_mask(create_request.account_number),
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return {
        "bank_account_id": str(account.bank_account_id),
        "bank_name": account.bank_name,
        "account_number_masked": account.account_number_masked,
    }


@router.delete('/{bank_account_id}', status_code=status.HTTP_200_OK)
async def delete_bank_account(bank_account_id: str, db: db_dependency, current_user: user_dependency):
    account = db.scalar(
        select(BankAccount).where(
            BankAccount.bank_account_id == bank_account_id,
            BankAccount.user_id == current_user.user_id,
        )
    )
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    db.delete(account)
    db.commit()
    return {"detail": "Bank account deleted"}


@router.get('/')
async def get_bank_accounts(db: db_dependency, current_user: user_dependency):
    accounts = db.scalars(
        select(BankAccount).where(BankAccount.user_id == current_user.user_id)
    ).all()
    return [
        {
            "bank_account_id": str(a.bank_account_id),
            "bank_name": a.bank_name,
            "account_number_masked": a.account_number_masked,
        }
        for a in accounts
    ]
