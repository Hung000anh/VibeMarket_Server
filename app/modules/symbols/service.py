from fastapi import HTTPException
from postgrest import APIError
from app.core.supabase_client import supabase_anon, supabase_service
from app.modules.symbols.schemas import SymbolRead, SymbolCreate, SymbolUpdate

# GET tất cả symbols
async def fetch_symbols() -> list[SymbolRead]:
    result = supabase_anon.table("symbols").select("*").execute()
    return [SymbolRead(**item) for item in result.data]

# POST tạo mới symbol
async def create_symbol(symbol: SymbolCreate) -> SymbolRead:
    result = supabase_service.table("symbols").insert(symbol.model_dump(mode='json')).execute()
    return SymbolRead(**result.data[0])

# PUT update symbol
async def update_symbol(id: str, symbol: SymbolUpdate) -> SymbolRead:
    try:
        result = supabase_service.table("symbols").update(symbol.model_dump(mode='json', exclude_unset=True)).eq("id", id).execute()
        return SymbolRead(**result.data[0])
    except APIError as e:
        if e.code == "23505":
            raise HTTPException(status_code=409, detail="Symbol already exists")
        raise

# DELETE symbol
async def delete_symbol(id: str) -> dict:
    result = supabase_service.table("symbols").delete().eq("id", id).execute()
    return {"deleted": len(result.data)}
