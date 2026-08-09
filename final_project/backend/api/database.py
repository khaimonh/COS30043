from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(override=True)

SQLALCHEMY_DATABASE_URL = os.getenv("SQL_ALCHEMY_DATABASE_URL")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

# Supabase pooler caps at 15 conns/session; keep sync+async pools under it
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=4,
    max_overflow=2,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=7,
    max_overflow=2,
    pool_pre_ping=True,
    connect_args={"statement_cache_size": 0},
)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
