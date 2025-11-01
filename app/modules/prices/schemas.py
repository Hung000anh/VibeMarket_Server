from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class PriceBase(BaseModel):
    symbol_timeframe_id: UUID
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float]
    recorded_at: datetime

class PriceCreate(PriceBase):
    pass

class PriceRead(PriceBase):
    id: UUID
