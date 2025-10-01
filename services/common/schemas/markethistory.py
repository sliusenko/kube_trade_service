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

    symbol_id: Optional[UUID] = None

    url: Optional[HttpUrl] = None
class NewsSentimentCreate(NewsSentimentBase):
    pass
class NewsSentimentUpdate(BaseModel):
    published_at: Optional[datetime] = None
    title: Optional[str] = Field(None, min_length=3, max_length=500)
    summary: Optional[str] = None
    sentiment: Optional[Decimal] = Field(None, ge=-1, le=1)
    source: Optional[str] = None

    symbol_id: Optional[UUID] = None

    url: Optional[HttpUrl] = None
class NewsSentimentOut(NewsSentimentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    price_before: Optional[Decimal] = None
    price_after_1h: Optional[Decimal] = None
    price_after_6h: Optional[Decimal] = None
    price_after_24h: Optional[Decimal] = None
    price_change_1h: Optional[float] = None
    price_change_6h: Optional[float] = None
    price_change_24h: Optional[float] = None
