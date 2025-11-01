from app.core.supabase_client import supabase_service
from app.modules.prices.schemas import PriceCreate, PriceRead

# Lấy toàn bộ giá
async def fetch_prices() -> list[PriceRead]:
    result = supabase_service.table("prices").select("*").execute()
    return [PriceRead(**row) for row in result.data]

# Lấy giá theo symbol_timeframe_id
async def fetch_prices_by_timeframe(symbol_timeframe_id: str) -> list[PriceRead]:
    result = (
        supabase_service.table("prices")
        .select("*")
        .eq("symbol_timeframe_id", symbol_timeframe_id)
        .execute()
    )
    return [PriceRead(**row) for row in result.data]

# Thêm nhiều bản ghi giá (OHLC)
async def create_prices(prices: list[PriceCreate]) -> list[PriceRead]:
    records = [p.model_dump(mode="json") for p in prices]
    result = (
        supabase_service
        .table("prices")
        .upsert(records, on_conflict="symbol_timeframe_id, recorded_at") 
        .execute()
    )
    return [PriceRead(**row) for row in result.data]