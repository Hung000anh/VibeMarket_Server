from fastapi import APIRouter
from typing import List
from app.modules.asset_types.service import create_asset_type, fetch_asset_types, update_asset_type, delete_asset_type
from app.modules.asset_types.schemas import AssetTypeRead, AssetTypeCreate, AssetTypeUpdate
router = APIRouter(prefix="/asset-types", tags=["Asset Types"])

@router.get("/", response_model=List[AssetTypeRead])
async def get_asset_types():
    return await fetch_asset_types()

@router.post("/", response_model=AssetTypeRead)
async def add_asset_type(asset_type: AssetTypeCreate):
    return await create_asset_type(asset_type)

@router.put("/{id}", response_model=AssetTypeRead)
async def edit_asset_type(id: str, asset_type: AssetTypeUpdate):
    return await update_asset_type(id, asset_type)

@router.delete("/{id}")
async def remove_asset_type(id: str):
    return await delete_asset_type(id)
