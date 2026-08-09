import os

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, stocks, portfolios, bank_accounts, orders, watchlist, admin, ws_quotes

from contextlib import asynccontextmanager
import threading

from api.services.price_poller import PricePoller
from api.services.order_queue import start_consumer
from api.services.trade_execution import execute_order

poller = PricePoller()

@asynccontextmanager
async def lifespan(app):
    await poller.start()
    consumer = threading.Thread(target=start_consumer, args=(execute_order,), daemon=True)
    consumer.start()
    yield
    await poller.stop()

app = FastAPI(lifespan=lifespan)

cors_env = os.getenv("CORS_ORIGINS", "")
origins = [
    origin.strip().strip('"').strip("'")
    for origin in cors_env.split(",")
    if origin
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return "Health check complete"



