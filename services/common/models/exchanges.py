import uuid
import datetime as dt
from typing import Optional, List, Dict, Any

from sqlalchemy import (
    BigInteger, SmallInteger, Text, Integer, Numeric, Boolean, TIMESTAMP,
    ForeignKey, UniqueConstraint, text, JSON
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Exchange(Base):
    __tablename__ = "exchanges"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'spot'"))
    environment: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'prod'"))

    base_url_public: Mapped[Optional[str]] = mapped_column(Text)
    base_url_private: Mapped[Optional[str]] = mapped_column(Text)
    ws_public_url: Mapped[Optional[str]] = mapped_column(Text)
    ws_private_url: Mapped[Optional[str]] = mapped_column(Text)
    data_feed_url: Mapped[Optional[str]] = mapped_column(Text)

    fetch_symbols_interval_min: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("60")
    )
    fetch_filters_interval_min: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1440")
    )
    fetch_limits_interval_min: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1440")
    )
    fetch_fees_interval_min: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1440")
    )

    rate_limit_per_min: Mapped[Optional[int]] = mapped_column(Integer)
    recv_window_ms: Mapped[int] = mapped_column(Integer, server_default=text("5000"))
    request_timeout_ms: Mapped[int] = mapped_column(Integer, server_default=text("10000"))

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )

    last_symbols_refresh_at: Mapped[Optional[dt.datetime]] = mapped_column(TIMESTAMP(timezone=True))
    last_filters_refresh_at: Mapped[Optional[dt.datetime]] = mapped_column(TIMESTAMP(timezone=True))
    last_fees_refresh_at: Mapped[Optional[dt.datetime]] = mapped_column(TIMESTAMP(timezone=True))
    last_limits_refresh_at: Mapped[Optional[dt.datetime]] = mapped_column(TIMESTAMP(timezone=True))

    status: Mapped[Optional[str]] = mapped_column(Text)
    status_msg: Mapped[Optional[str]] = mapped_column(Text)

    features: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, server_default=text("'{}'::jsonb")
    )
    extra: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, server_default=text("'{}'::jsonb")
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # relationships
    credentials: Mapped[List["ExchangeCredential"]] = relationship(  # type: ignore[name-defined]
        back_populates="exchange", cascade="all, delete-orphan"
    )
    symbols: Mapped[List["ExchangeSymbol"]] = relationship(  # type: ignore[name-defined]
        back_populates="exchange", cascade="all, delete-orphan"
    )
    limits: Mapped[List["ExchangeLimit"]] = relationship(  # type: ignore[name-defined]
        back_populates="exchange", cascade="all, delete-orphan"
    )
    status_history: Mapped[List["ExchangeStatusHistory"]] = relationship(  # type: ignore[name-defined]
        back_populates="exchange", cascade="all, delete-orphan"
    )
    fees: Mapped[List["ExchangeFee"]] = relationship(  # type: ignore[name-defined]
        back_populates="exchange", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Exchange {self.code} ({self.environment}) active={self.is_active}>"
class ExchangeCredential(Base):
    __tablename__ = "exchange_credentials"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )

    label: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_service: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )

    api_key: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    api_secret: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    api_passphrase: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    subaccount: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scopes: Mapped[List[str]] = mapped_column(
        JSONB, server_default=text("'[]'::jsonb"), nullable=False
    )

    secret_ref: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    vault_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    valid_from: Mapped[Optional[dt.datetime]] = mapped_column(TIMESTAMP(timezone=True))
    valid_to: Mapped[Optional[dt.datetime]] = mapped_column(TIMESTAMP(timezone=True))

    created_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # 🔗 relationships
    exchange: Mapped["Exchange"] = relationship(  # type: ignore[name-defined]
        back_populates="credentials"
    )

    def __repr__(self) -> str:
        return f"<ExchangeCredential {self.id} exchange={self.exchange_id} active={self.is_active}>"
class ExchangeSymbol(Base):
    __tablename__ = "exchange_symbols"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol_id: Mapped[str] = mapped_column(Text, nullable=False)
    symbol: Mapped[str] = mapped_column(Text, nullable=False)

    base_asset: Mapped[str] = mapped_column(Text, nullable=False)
    quote_asset: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(Text, server_default=text("'spot'"))

    base_precision: Mapped[Optional[int]] = mapped_column(Integer)
    quote_precision: Mapped[Optional[int]] = mapped_column(Integer)
    step_size: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tick_size: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    min_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    max_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    min_notional: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    max_notional: Mapped[Optional[Decimal]] = mapped_column(Numeric)

    filters: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, server_default=text("'{}'::jsonb"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )

    fetched_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # 🔗 relationships
    exchange: Mapped["Exchange"] = relationship(  # type: ignore[name-defined]
        back_populates="symbols"
    )
    fees: Mapped[List["ExchangeFee"]] = relationship(  # type: ignore[name-defined]
        back_populates="symbol", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("exchange_id", "symbol_id", name="uq_exchange_symbol"),
    )

    def __repr__(self) -> str:
        return f"<ExchangeSymbol {self.symbol} ({self.base_asset}/{self.quote_asset}) active={self.is_active}>"

class ExchangeFee(Base):
    __tablename__ = "exchange_fees"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id", ondelete="CASCADE"))
    symbol_id   = Column(BigInteger, ForeignKey("exchange_symbols.id", ondelete="CASCADE"), nullable=True)

    volume_threshold = Column(Numeric, nullable=False)
    maker_fee = Column(Numeric, nullable=True)
    taker_fee = Column(Numeric, nullable=True)

    fetched_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    exchange = relationship("Exchange", back_populates="fees")
    symbol   = relationship("ExchangeSymbol", back_populates="fees")


class ExchangeLimit(Base):
    __tablename__ = "exchange_limits"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id", ondelete="CASCADE"))
    limit_type   = Column(Text, nullable=False)
    interval_unit = Column(Text, nullable=False)
    interval_num  = Column(Integer, nullable=False)
    limit        = Column(Integer, nullable=False)

    raw_json = Column(JSONB, server_default="{}")
    fetched_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    exchange = relationship("Exchange", back_populates="limits")


class ExchangeStatusHistory(Base):
    __tablename__ = "exchange_status_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id", ondelete="CASCADE"), nullable=False)

    event   = Column(Text, nullable=False)
    status  = Column(Text, nullable=False)
    message = Column(Text)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    exchange = relationship("Exchange", back_populates="status_history")
