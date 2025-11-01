from fastapi import APIRouter
from typing import List
from app.modules.exchanges.service import fetch_exchanges, create_exchange, update_exchange, delete_exchange
from app.modules.exchanges.schemas import ExchangeRead, ExchangeCreate, ExchangeUpdate

router = APIRouter(prefix="/exchanges", tags=["Exchanges"])

@router.get("/", response_model=List[ExchangeRead])
async def get_exchanges():
    return await fetch_exchanges()

@router.post("/", response_model=ExchangeRead)
async def add_exchange(exchange: ExchangeCreate):
    return await create_exchange(exchange)

@router.put("/{id}", response_model=ExchangeRead)
async def edit_exchange(id: str, exchange: ExchangeUpdate):
    return await update_exchange(id, exchange)

@router.delete("/{id}")
async def remove_exchange(id: str):
    return await delete_exchange(id)
