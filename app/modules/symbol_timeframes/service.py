from app.core.supabase_client import supabase_anon, supabase_service
from app.modules.symbol_timeframes.schemas import SymbolTimeframeRead, SymbolTimeframeCreate, SymbolTimeframeUpdate

# GET tất cả
async def fetch_symbol_timeframes() -> list[SymbolTimeframeRead]:
    result = supabase_anon.table("symbol_timeframes").select("*").execute()
    return [SymbolTimeframeRead(**item) for item in result.data]

# POST tạo mới
async def create_symbol_timeframes(st: SymbolTimeframeCreate) -> list[SymbolTimeframeRead]:
    records = [{"symbol_id": str(st.symbol_id), "timeframe_id": str(tid)} for tid in st.timeframe_ids]
    result = supabase_service.table("symbol_timeframes").insert(records, on_conflict=["symbol_id", "timeframe_id"]).execute()
    return [SymbolTimeframeRead(**item) for item in result.data]

# PUT update
async def update_symbol_timeframe(id: str, st: SymbolTimeframeUpdate) -> SymbolTimeframeRead:
    result = supabase_service.table("symbol_timeframes").update(st.model_dump(mode='json', exclude_unset=True)).eq("id", id).execute()
    return SymbolTimeframeRead(**result.data[0])

# DELETE
async def delete_symbol_timeframe(id: str) -> dict:
    result = supabase_service.table("symbol_timeframes").delete().eq("id", id).execute()
    return {"deleted": len(result.data)}