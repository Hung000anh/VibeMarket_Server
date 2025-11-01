from fastapi import APIRouter
from typing import List
from app.modules.symbol_timeframes.service import fetch_symbol_timeframes, create_symbol_timeframes, update_symbol_timeframe, delete_symbol_timeframe
from app.modules.symbol_timeframes.schemas import SymbolTimeframeRead, SymbolTimeframeCreate, SymbolTimeframeUpdate

router = APIRouter(prefix="/symbol-timeframes", tags=["Symbol Timeframes"])

@router.get("/", response_model=List[SymbolTimeframeRead])
async def get_symbol_timeframes():
    return await fetch_symbol_timeframes()

@router.post("/", response_model=List[SymbolTimeframeRead])
async def add_symbol_timeframe(st: SymbolTimeframeCreate):
    return await create_symbol_timeframes(st)

@router.put("/{id}", response_model=SymbolTimeframeRead)
async def edit_symbol_timeframe(id: str, st: SymbolTimeframeUpdate):
    return await update_symbol_timeframe(id, st)

@router.delete("/{id}")
async def remove_symbol_timeframe(id: str):
    return await delete_symbol_timeframe(id)