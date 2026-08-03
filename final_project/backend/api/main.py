from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, stocks, portfolios, bank_accounts, orders

from contextlib import asynccontextmanager
from api.services.price_poller import PricePoller

poller = PricePoller()

@asynccontextmanager
async def lifespan(app):
    await poller.start()
    yield
    await poller.stop()

# app = FastAPI()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(stocks.router)
app.include_router(portfolios.router)
app.include_router(bank_accounts.router)
app.include_router(orders.router)

@app.get("/")
def health_check():
    return "Health check complete"



