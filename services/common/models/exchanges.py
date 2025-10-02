import uuid
import datetime as dt
from decimal import Decimal
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

    use_service_symbol: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

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
    trade_profiles: Mapped[List["TradeProfile"]] = relationship(
        "TradeProfile", back_populates="exchange", cascade="all, delete"
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

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    symbol_id: Mapped[str] = mapped_column(Text, nullable=False)

    # # якщо хочеш, щоб унікальність була глобально:
    # symbol: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    symbol: Mapped[str] = mapped_column(Text, nullable=False)

    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )

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
    exchange: Mapped["Exchange"] = relationship(back_populates="symbols")
    fees: Mapped[List["ExchangeFee"]] = relationship(
        back_populates="symbol", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("exchange_id", "symbol_id", name="uq_exchange_symbol"),
    )

    def __repr__(self) -> str:
        return f"<ExchangeSymbol {self.symbol} ({self.base_asset}/{self.quote_asset}) active={self.is_active}>"
class ExchangeFee(Base):
    __tablename__ = "exchange_fees"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchange_symbols.id", ondelete="CASCADE"),
        nullable=True,
    )

    volume_threshold: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    maker_fee: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    taker_fee: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    fetched_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()")
    )

    # 🔗 relationships
    exchange: Mapped["Exchange"] = relationship(back_populates="fees")
    symbol: Mapped[Optional["ExchangeSymbol"]] = relationship(back_populates="fees")

    __table_args__ = (
        UniqueConstraint("exchange_id", "symbol_id", "volume_threshold", name="uq_exchange_fee"),
    )

    def __repr__(self) -> str:
        return f"<ExchangeFee {self.exchange_id} symbol={self.symbol_id} maker={self.maker_fee} taker={self.taker_fee}>"
class ExchangeLimit(Base):
    __tablename__ = "exchange_limits"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )

    limit_type: Mapped[str] = mapped_column(Text, nullable=False)
    interval_unit: Mapped[str] = mapped_column(Text, nullable=False)
    interval_num: Mapped[int] = mapped_column(Integer, nullable=False)
    limit: Mapped[int] = mapped_column(Integer, nullable=False)

    raw_json: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, server_default=text("'{}'::jsonb"), nullable=False
    )
    fetched_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # 🔗 relationships
    exchange: Mapped["Exchange"] = relationship(  # type: ignore[name-defined]
        back_populates="limits"
    )

    __table_args__ = (
        UniqueConstraint("exchange_id", "limit_type", "interval_unit", "interval_num", name="uq_exchange_limit"),
    )

    def __repr__(self) -> str:
        return f"<ExchangeLimit {self.exchange_id} {self.limit_type} {self.interval_num}{self.interval_unit}={self.limit}>"
class ExchangeStatusHistory(Base):
    __tablename__ = "exchange_status_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )

    event: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # 🔗 relationships
    exchange: Mapped["Exchange"] = relationship(  # type: ignore[name-defined]
        back_populates="status_history"
    )

    def __repr__(self) -> str:
        return f"<ExchangeStatusHistory {self.exchange_id} {self.event} {self.status}>"
