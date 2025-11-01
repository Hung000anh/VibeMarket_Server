from pydantic import BaseModel
from uuid import UUID

class ExchangeRead(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }

class ExchangeCreate(BaseModel):
    name: str

class ExchangeUpdate(BaseModel):
    name: str