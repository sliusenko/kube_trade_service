# app/models/price_history.py
import datetime as dt
from decimal import Decimal
from typing import Optional
from sqlalchemy import BigInteger, Text, Numeric, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column

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
    __tablename__ = "news_sentiment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    published_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sentiment: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    symbol: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<NewsSentiment {self.published_at} {self.title[:30]!r}...>"
