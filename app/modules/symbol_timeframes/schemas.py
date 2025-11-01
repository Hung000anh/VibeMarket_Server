from pydantic import BaseModel
from uuid import UUID

class SymbolTimeframeRead(BaseModel):
    id: UUID
    symbol_id: UUID
    timeframe_id: UUID

    model_config = {
        "from_attributes": True,
    }

class SymbolTimeframeCreate(BaseModel):
    symbol_id: UUID
    timeframe_ids: list[UUID]

class SymbolTimeframeUpdate(BaseModel):
    symbol_id: UUID | None = None
    timeframe_id: UUID | None = None
