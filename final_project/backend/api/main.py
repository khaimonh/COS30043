import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, stocks, portfolios, bank_accounts, orders, watchlist, admin, ws_quotes

from contextlib import asynccontextmanager
from api.services.price_poller import PricePoller

poller = PricePoller()

@asynccontextmanager
async def lifespan(app):
    await poller.start()
    yield
    await poller.stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(stocks.router)
app.include_router(portfolios.router)
app.include_router(bank_accounts.router)
app.include_router(orders.router)
app.include_router(watchlist.router)
app.include_router(admin.router)
app.include_router(ws_quotes.router)

@app.get("/")
def health_check():
    return "Health check complete"



