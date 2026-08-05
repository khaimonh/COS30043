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
    Enum,
    CheckConstraint,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from api.database import Base


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )
    role_name: Mapped[str] = mapped_column(String(30))

    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"Role: (id={self.role_id}, name={self.role_name})"


class UserStatus(enum.Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_email"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.role_id"))
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status"), nullable=False, default=UserStatus.ACTIVE
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    role: Mapped["Role"] = relationship(back_populates="users")
    portfolios: Mapped[list["Portfolio"]] = relationship(back_populates="user")
    bank_accounts: Mapped[list["BankAccount"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    watchlists: Mapped[list["Watchlist"]] = relationship(back_populates="user")


# every user will have these
class Portfolio(Base):
    __tablename__ = "portfolio"

    portfolio_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"))
    name: Mapped[str] = mapped_column(String(255))
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    version: Mapped[int] = mapped_column(Integer, default=0)

    __mapper_args__ = {"version_id_col": version}

    user: Mapped["User"] = relationship(back_populates="portfolios")
    cash_transactions: Mapped[list["CashTransaction"]] = relationship(back_populates="portfolio", passive_deletes=True)
    holdings: Mapped[list["Holding"]] = relationship(back_populates="portfolio", passive_deletes=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="portfolio", passive_deletes=True)


class BankAccount(Base):
    __tablename__ = "bank_account"

    bank_account_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"))
    account_number_encrypted: Mapped[str] = mapped_column(EncryptedString())
    account_number_masked: Mapped[str] = mapped_column(String(255))
    bank_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="bank_accounts")
    cash_transactions: Mapped[list["CashTransaction"]] = relationship(back_populates="bank_account")


class CashTransactionType(enum.Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"


class CashTransaction(Base):
    __tablename__ = "cash_transactions"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4 ,
    )

    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("portfolio.portfolio_id", ondelete="CASCADE"),
    )

    bank_account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("bank_account.bank_account_id", ondelete="SET NULL"),
        nullable=True,
    )

    type: Mapped[CashTransactionType] = mapped_column(
        Enum(CashTransactionType, name="cash_transaction_type"),
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    portfolio: Mapped["Portfolio"] = relationship(back_populates="cash_transactions")
    bank_account: Mapped["BankAccount"] = relationship(back_populates="cash_transactions")


class Stock(Base):
    __tablename__ = "stocks"

    stock_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4 ,
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

    listing_date: Mapped[Optional[DateTime]] = mapped_column(
          DateTime(timezone=True), nullable=True
      )
    
    listed: Mapped[bool] = mapped_column(
        nullable=False, default=True, server_default="true"
    )
    # Relationships
    holdings: Mapped[list["Holding"]] = relationship(back_populates="stock")
    orders: Mapped[list["Order"]] = relationship(back_populates="stock")
    price_history: Mapped[list["PriceHistory"]] = relationship(
        back_populates="stock",
        cascade="all, delete-orphan",
    )
    watchlists: Mapped[list["Watchlist"]] = relationship(back_populates="stock")


class PriceHistory(Base):
    __tablename__ = "price_history"

    history_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4 ,
    )

    stock_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("stocks.stock_id", ondelete="CASCADE"),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    open_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    high_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    low_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    volume: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    recorded_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    stock: Mapped["Stock"] = relationship(back_populates="price_history")


class Holding(Base):
    """
    Per-lot holding. A buy creates a new lot with full `original_quantity`;
    sells consume from lots via HoldingAllocation, decrementing `remaining_quantity`.
    Lots are never merged.
    """
    __tablename__ = "holdings"
    __table_args__ = (
        CheckConstraint("original_quantity > 0", name="ck_holding_original_qty_pos"),
        CheckConstraint("remaining_quantity >= 0", name="ck_holding_remaining_qty_nonneg"),
        CheckConstraint(
            "remaining_quantity <= original_quantity",
            name="ck_holding_remaining_le_original",
        ),
        CheckConstraint("purchase_price >= 0", name="ck_holding_purchase_price_nonneg"),
    )

    holding_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )

    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("portfolio.portfolio_id", ondelete="CASCADE"),
        nullable=False,
    )

    stock_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("stocks.stock_id", ondelete="RESTRICT"),
        nullable=False,
    )

    purchase_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    original_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    remaining_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __mapper_args__ = {"version_id_col": version}

    portfolio: Mapped["Portfolio"] = relationship(back_populates="holdings")
    stock: Mapped["Stock"] = relationship(back_populates="holdings")
    allocations: Mapped[list["HoldingAllocation"]] = relationship(back_populates="holding")


class OrderType(enum.Enum):
    BUY = "Buy"
    SELL = "Sell"


class OrderStyle(enum.Enum):
    MARKET = "Market"
    LIMIT = "Limit"


class OrderStatus(enum.Enum):
    PENDING = "Pending"
    FILLED = "Filled"
    CANCELLED = "Cancelled"
    REJECTED = "Rejected"


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_quantity_pos"),
        CheckConstraint(
            "(order_style = 'LIMIT' AND limit_price IS NOT NULL) OR "
            "(order_style <> 'LIMIT')",
            name="ck_order_limit_price_required",
        ),
    )

    order_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("portfolio.portfolio_id", ondelete="CASCADE"),
        nullable=False,
    )
    stock_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("stocks.stock_id", ondelete="RESTRICT"),
        nullable=False,
    )

    order_type: Mapped[OrderType] = mapped_column(Enum(OrderType, name="order_type"), nullable=False)
    order_style: Mapped[OrderStyle] = mapped_column(
        Enum(OrderStyle, name="order_style"), nullable=False
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"),
        nullable=False,
        default=OrderStatus.PENDING,
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="orders")
    portfolio: Mapped["Portfolio"] = relationship(back_populates="orders")
    stock: Mapped["Stock"] = relationship(back_populates="orders")
    trades: Mapped[list["Trade"]] = relationship(back_populates="order")


class Trade(Base):
    """
    Execution record. One order can produce multiple trades (partial fills).
    A sell trade consumes lots via HoldingAllocation.
    """
    __tablename__ = "trades"
    __table_args__ = (
        CheckConstraint("executed_quantity > 0", name="ck_trade_executed_qty_pos"),
        CheckConstraint("execution_price >= 0", name="ck_trade_execution_price_nonneg"),
    )

    trade_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    execution_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    executed_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    executed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    order: Mapped["Order"] = relationship(back_populates="trades")
    allocations: Mapped[list["HoldingAllocation"]] = relationship(back_populates="trade")


class HoldingAllocation(Base):
    """
    Join between Trade (a sell) and Holding (the lot consumed).
    Empty for buy trades; sells may span multiple lots (FIFO).
    """
    __tablename__ = "holding_allocations"
    __table_args__ = (
        CheckConstraint("quantity_consumed > 0", name="ck_allocation_qty_pos"),
    )

    allocation_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )

    trade_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("trades.trade_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    holding_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("holdings.holding_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quantity_consumed: Mapped[int] = mapped_column(Integer, nullable=False)

    trade: Mapped["Trade"] = relationship(back_populates="allocations")
    holding: Mapped["Holding"] = relationship(back_populates="allocations")


class Watchlist(Base):
    __tablename__ = "watchlist"
    __table_args__ = (
        UniqueConstraint("user_id", "stock_id", name="uq_watchlist_user_stock"),
        CheckConstraint(
            "target_price IS NULL OR target_price >= 0",
            name="ck_watchlist_target_price_nonneg",
        ),
    )

    watchlist_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4 )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    stock_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("stocks.stock_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    target_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="watchlists")
    stock: Mapped["Stock"] = relationship(back_populates="watchlists")
