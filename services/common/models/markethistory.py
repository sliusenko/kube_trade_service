# app/models/price_history.py
import uuid
import datetime as dt
from decimal import Decimal
from typing import Optional
from sqlalchemy import (
    BigInteger, Text, Numeric, TIMESTAMP, text,
    Column, String, DateTime, Float, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from .base import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    exchange: Mapped[str] = mapped_column(Text, nullable=False)
    symbol: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    timestamp: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    def __repr__(self) -> str:
        return f"<PriceHistory {self.exchange}:{self.symbol} {self.price} @ {self.timestamp}>"

class NewsSentiment(Base):
    __tablename__ = "news_sentiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(String(1000))
    sentiment = Column(Float)
    source = Column(String(80))
    symbol = Column(String(20), index=True, nullable=True)
    url = Column(String(500))

    # ✅ нові поля для прайсів і відсоткових змін
    price_before   = Column(Numeric(18, 8))
    price_after_1h = Column(Numeric(18, 8))
    price_after_6h = Column(Numeric(18, 8))
    price_after_24h= Column(Numeric(18, 8))
    price_change_1h = Column(Float)
    price_change_6h = Column(Float)
    price_change_24h= Column(Float)

    __table_args__ = (
        UniqueConstraint("published_at", "title", name="uq_news_ts_title"),
    )