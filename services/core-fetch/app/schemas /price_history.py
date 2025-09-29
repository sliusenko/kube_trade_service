from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PriceHistoryBase(BaseModel):
    timestamp: datetime
    exchange: str
    pair: str
    price: float

class PriceHistoryCreate(PriceHistoryBase):
    pass

class PriceHistoryInDB(PriceHistoryBase):
    id: int

    class Config:
        orm_mode = True
