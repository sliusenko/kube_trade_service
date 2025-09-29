from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsSentimentBase(BaseModel):
    published_at: datetime
    title: str
    summary: Optional[str] = None
    sentiment: Optional[float] = None
    source: Optional[str] = None
    pair: Optional[str] = None
    url: Optional[str] = None

class NewsSentimentCreate(NewsSentimentBase):
    pass

class NewsSentimentUpdate(BaseModel):
    sentiment: Optional[float] = None
    price_before: Optional[float] = None
    price_after_1h: Optional[float] = None
    price_after_6h: Optional[float] = None
    price_after_24h: Optional[float] = None
    price_change_1h: Optional[float] = None
    price_change_6h: Optional[float] = None
    price_change_24h: Optional[float] = None

class NewsSentimentInDB(NewsSentimentBase):
    id: int
    price_before: Optional[float] = None
    price_after_1h: Optional[float] = None
    price_after_6h: Optional[float] = None
    price_after_24h: Optional[float] = None
    price_change_1h: Optional[float] = None
    price_change_6h: Optional[float] = None
    price_change_24h: Optional[float] = None

    class Config:
        orm_mode = True
