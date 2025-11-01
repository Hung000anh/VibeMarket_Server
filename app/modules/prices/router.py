from fastapi import APIRouter
from typing import List
from app.modules.prices.service import fetch_prices, fetch_prices_by_timeframe, create_prices
from app.modules.prices.schemas import PriceRead, PriceCreate

router = APIRouter(prefix="/prices", tags=["Prices"])

@router.get("/", response_model=List[PriceRead])
async def get_prices():
    return await fetch_prices()

@router.get("/{symbol_timeframe_id}")
async def get_prices_by_timeframe(symbol_timeframe_id: str):
    return await fetch_prices_by_timeframe(symbol_timeframe_id)

@router.post("/", response_model=List[PriceRead])
async def add_prices(prices: List[PriceCreate]):
    return await create_prices(prices)
