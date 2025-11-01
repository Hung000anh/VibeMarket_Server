from fastapi import APIRouter
from typing import List
from app.modules.timeframes.service import fetch_timeframes, create_timeframe, update_timeframe, delete_timeframe
from app.modules.timeframes.schemas import TimeframeRead, TimeframeCreate, TimeframeUpdate

router = APIRouter(prefix="/timeframes", tags=["Timeframes"])

@router.get("/", response_model=List[TimeframeRead])
async def get_timeframes():
    return await fetch_timeframes()

@router.post("/", response_model=TimeframeRead)
async def add_timeframe(timeframe: TimeframeCreate):
    return await create_timeframe(timeframe)

@router.put("/{id}", response_model=TimeframeRead)
async def edit_timeframe(id: str, timeframe: TimeframeUpdate):
    return await update_timeframe(id, timeframe)

@router.delete("/{id}")
async def remove_timeframe(id: str):
    return await delete_timeframe(id)