from pydantic import BaseModel
from uuid import UUID

class SymbolRead(BaseModel):
    id: UUID
    symbol: str
    name: str
    exchange_id: UUID
    asset_type_id: UUID

    model_config = {
        "from_attributes": True
    }

class SymbolCreate(BaseModel):
    symbol: str
    name: str
    exchange_id: UUID
    asset_type_id: UUID

class SymbolUpdate(BaseModel):
    symbol: str | None = None
    name: str | None = None
    exchange_id: UUID | None = None
    asset_type_id: UUID | None = None
