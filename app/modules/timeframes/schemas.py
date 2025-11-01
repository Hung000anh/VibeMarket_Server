from pydantic import BaseModel, UUID4

class TimeframeBase(BaseModel):
    name: str

class TimeframeCreate(TimeframeBase):
    pass

class TimeframeUpdate(BaseModel):
    name: str | None = None

class TimeframeRead(TimeframeBase):
    id: UUID4