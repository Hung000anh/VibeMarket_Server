from fastapi import HTTPException
from postgrest import APIError
from app.core.supabase_client import supabase_service, supabase_anon

async def fetch_timeframes():
    result = supabase_anon.table("timeframes").select("*").execute()
    return result.data

async def create_timeframe(timeframe):
    try:
        result = supabase_service.table("timeframes").insert(timeframe.model_dump(mode='json')).execute()
        return result.data[0]
    except APIError as e:
        if e.code == "23505":
            raise HTTPException(status_code=409, detail="Timeframe already exists")
        raise

async def update_timeframe(id: str, timeframe):
    result = supabase_service.table("timeframes").update(timeframe.model_dump(exclude_unset=True)).eq("id", id).execute()
    return result.data[0] if result.data else None

async def delete_timeframe(id: str):
    result = supabase_service.table("timeframes").delete().eq("id", id).execute()
    return {"deleted": len(result.data) > 0}