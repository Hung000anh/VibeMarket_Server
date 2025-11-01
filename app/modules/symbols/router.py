from fastapi import APIRouter
from typing import List
from app.modules.symbols.service import fetch_symbols, create_symbol, update_symbol, delete_symbol
from app.modules.symbols.schemas import SymbolRead, SymbolCreate, SymbolUpdate

router = APIRouter(prefix="/symbols", tags=["Symbols"])

@router.get("/", response_model=List[SymbolRead])
async def get_symbols():
    return await fetch_symbols()

@router.post("/", response_model=SymbolRead)
async def add_symbol(symbol: SymbolCreate):
    return await create_symbol(symbol)

@router.put("/{id}", response_model=SymbolRead)
async def edit_symbol(id: str, symbol: SymbolUpdate):
    return await update_symbol(id, symbol)

@router.delete("/{id}")
async def remove_symbol(id: str):
    return await delete_symbol(id)
