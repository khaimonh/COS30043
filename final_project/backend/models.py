from decimal import Decimal
from typing import Optional
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String,
    Table,
    Text,
    DateTime,
    UniqueConstraint,
    func,
    select
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
    
    portfolios: Mapped[list["Portfolio"]] = relationship(back_populates="user")

#every user will have these
class Portfolio(Base):
    __tablename__= "portfolio"

    portfolio_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    name: Mapped[str] = mapped_column(String(255))
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    version: Mapped[int] = mapped_column(int)
    
class BankAccount(Base):
    __tablename__=  "bank_account"

    bank_account_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    account_number: Mapped

