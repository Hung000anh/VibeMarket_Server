from pydantic import BaseModel
from uuid import UUID

class AssetTypeRead(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }

class AssetTypeCreate(BaseModel):
    name: str

class AssetTypeUpdate(BaseModel):
    name: str
