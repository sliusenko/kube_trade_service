import uuid
import datetime as dt
from decimal import Decimal
from sqlalchemy import (
    BigInteger, Text, Numeric, TIMESTAMP, text,
    Column, String, DateTime, Float, UniqueConstraint
)
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )

    # ✅ Тепер зберігаємо UUID біржі
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ✅ символ лишається UUID (як і було)
    symbol: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchange_symbols.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)

    timestamp: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        index=True
    )

    def __repr__(self) -> str:
        return f"<PriceHistory {self.exchange_id}:{self.symbol} {self.price} @ {self.timestamp}>"

class NewsSentiment(Base):
    __tablename__ = "news_sentiments"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
    )
    title: Mapped[str] = mapped_column(sa.Text, nullable=False)
    sentiment: Mapped[float] = mapped_column(sa.Numeric, nullable=False)
    source: Mapped[str] = mapped_column(sa.String, nullable=False)
    url: Mapped[str] = mapped_column(sa.Text, nullable=False)

    # 🔄 symbol → symbol_id
    symbol_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        sa.ForeignKey("exchange_symbols.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    summary = Column(String(1000))

    price_before    = Column(Numeric(18, 8))
    price_after_1h  = Column(Numeric(18, 8))
    price_after_6h  = Column(Numeric(18, 8))
    price_after_24h = Column(Numeric(18, 8))

    price_change_1h  = Column(Float)
    price_change_6h  = Column(Float)
    price_change_24h = Column(Float)

    __table_args__ = (
        UniqueConstraint("published_at", "title", name="uq_news_ts_title"),
    )