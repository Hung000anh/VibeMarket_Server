from fastapi import HTTPException
from postgrest import APIError
from app.core.supabase_client import supabase_anon, supabase_service
from app.modules.exchanges.schemas import ExchangeRead, ExchangeCreate, ExchangeUpdate

# GET danh sách exchanges
async def fetch_exchanges() -> list[ExchangeRead]:
    result = supabase_anon.table("exchanges").select("*").execute()
    return [ExchangeRead(**item) for item in result.data]

# POST tạo mới
async def create_exchange(exchange: ExchangeCreate) -> ExchangeRead:
    try:
        result = supabase_service.table("exchanges").insert(exchange.model_dump()).execute()
        return ExchangeRead(**result.data[0])
    except APIError as e:
        # kiểm tra mã lỗi unique violation của PostgreSQL
        if e.code == "23505":
            raise HTTPException(status_code=409, detail="Exchange already exists")
        raise


# PUT cập nhật
async def update_exchange(id: str, exchange: ExchangeUpdate) -> ExchangeRead:
    result = supabase_service.table("exchanges").update(exchange.model_dump()).eq("id", id).execute()
    return ExchangeRead(**result.data[0])

# DELETE
async def delete_exchange(id: str) -> dict:
    result = supabase_service.table("exchanges").delete().eq("id", id).execute()
    return {"deleted": len(result.data)}
