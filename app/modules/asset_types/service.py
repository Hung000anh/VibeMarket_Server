from fastapi import HTTPException
from postgrest import APIError
from app.core.supabase_client import supabase_anon, supabase_service
from app.modules.asset_types.schemas import AssetTypeRead, AssetTypeCreate, AssetTypeUpdate

# GET: lấy tất cả, dùng anon key
async def fetch_asset_types() -> list[AssetTypeRead]:
    result = supabase_anon.table("asset_types").select("*").execute()
    return [AssetTypeRead(**item) for item in result.data]

# POST: tạo mới, dùng service role key
async def create_asset_type(asset_type: AssetTypeCreate) -> AssetTypeRead:
    try:
        result = supabase_service.table("asset_types").insert(asset_type.model_dump()).execute()
        return AssetTypeRead(**result.data[0])
    except APIError as e:
        # kiểm tra mã lỗi unique violation của PostgreSQL
        if e.code == "23505":
            raise HTTPException(status_code=409, detail="Asset type already exists")
        raise

# PUT: cập nhật, dùng service role key
async def update_asset_type(id: str, asset_type: AssetTypeUpdate) -> AssetTypeRead:
    result = supabase_service.table("asset_types")\
        .update(asset_type.model_dump()).eq("id", id).execute()
    return AssetTypeRead(**result.data[0])

# DELETE: xóa, dùng service role key
async def delete_asset_type(id: str) -> dict:
    result = supabase_service.table("asset_types").delete().eq("id", id).execute()
    return {"deleted": len(result.data)}