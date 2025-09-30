from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from sqlalchemy import Column, BigInteger, Text, Numeric, TIMESTAMP, text
from common.models.base import Base

class PriceHistoryBase(BaseModel):
    exchange: str
    symbol: str
    price: Decimal = Field(..., gt=0)
class PriceHistoryCreate(PriceHistoryBase):
    timestamp: Optional[datetime] = None 
class PriceHistoryOut(PriceHistoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
class NewsSentimentBase(BaseModel):
    published_at: datetime
    title: str = Field(..., min_length=3, max_length=500)
    summary: Optional[str] = None
    sentiment: Optional[Decimal] = Field(None, ge=-1, le=1)  
    source: Optional[str] = None
    symbol: Optional[str] = None
    url: Optional[HttpUrl] = None
class NewsSentimentCreate(NewsSentimentBase):
    pass
class NewsSentimentOut(NewsSentimentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
