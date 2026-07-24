from decimal import Decimal
from typing import Optional

from utils.models.encrypt import EncryptedString 
import uuid
import enum

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
    DateTime,
    UniqueConstraint,
    func,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session

from database import Base

class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    role_name: Mapped[str] = mapped_column(String(30))

    users: Mapped["User"] = relationship(back_populates="role")

    def __repr__(self):
        return f"Role: (id={self.role_id}, name={self.role_name})"
    
class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_email")
    )

    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.role_id"))
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    portfolios: Mapped[list["Portfolio"]] = relationship(back_populates="users")

#every user will have these
class Portfolio(Base):
    __tablename__= "portfolio"

    portfolio_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    name: Mapped[str] = mapped_column(String(255))
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    version: Mapped[int] = mapped_column(int)

    cash_transaction: Mapped[list["CashTransaction"]] = relationship(back_populates="portfolio")
    
class BankAccount(Base):
    __tablename__=  "bank_account"

    bank_account_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    account_number: Mapped[str] = mapped_column(EncryptedString())
    routing_number: Mapped[Optional[str]] = mapped_column(EncryptedString(), nullable=True)
    bank_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="bank_account")

class CashTransactionType(enum.Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"


class CashTransaction(Base):
    __tablename__ = "cash_transactions"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4(),
    )

    portfolio_id: Mapped[UUID] = mapped_column(
        ForeignKey("portfolios.portfolio_id", ondelete="CASCADE"),
    )

    bank_account_id: Mapped[UUID] = mapped_column(
        ForeignKey("bank_account.bank_account_id", ondelete="SET NULL"),
    )

    type: Mapped[CashTransactionType] = mapped_column(
        Enum(CashTransactionType, name="cash_transaction_type"),
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    portfolio: Mapped["Portfolio"] = relationship(back_populates="cash_transaction")

    bank_account: Mapped["BankAccount"] = relationship(back_populates="cash_transaction")

class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4(),
    )

    ticker: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    exchange: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    sector: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Relationships
    holdings = relationship(
        "Holding",
        back_populates="stock",
    )

    orders = relationship(
        "Order",
        back_populates="stock",
    )

    price_history = relationship(
        "StockPrice",
        back_populates="stock",
        cascade="all, delete-orphan",
    )


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4(),
    )

    stock_id: Mapped[UUID] = mapped_column(
        ForeignKey("stocks.id", ondelete="CASCADE"),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    recorded_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    stock = relationship(
        "Stock",
        back_populates="price_history",
    )