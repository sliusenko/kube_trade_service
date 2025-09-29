import uuid
from sqlalchemy import (
    Column, BigInteger, Numeric, Text, Boolean, Integer, SmallInteger,
    ForeignKey, TIMESTAMP, UniqueConstraint, text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base


class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    kind = Column(Text, nullable=False, server_default=text("'spot'"))
    environment = Column(Text, nullable=False, server_default=text("'prod'"))

    base_url_public  = Column(Text)
    base_url_private = Column(Text)
    ws_public_url    = Column(Text)
    ws_private_url   = Column(Text)
    data_feed_url    = Column(Text)

    fetch_symbols_interval_min = Column(SmallInteger, nullable=False, server_default=text("60"))
    fetch_filters_interval_min = Column(SmallInteger, nullable=False, server_default=text("1440"))
    fetch_limits_interval_min  = Column(SmallInteger, nullable=False, server_default=text("1440"))
    fetch_fees_interval_min    = Column(SmallInteger, nullable=False, server_default=text("1440"))

    rate_limit_per_min = Column(Integer)
    recv_window_ms     = Column(Integer, server_default=text("5000"))
    request_timeout_ms = Column(Integer, server_default=text("10000"))

    is_active = Column(Boolean, nullable=False, server_default=text("true"))

    last_symbols_refresh_at = Column(TIMESTAMP(timezone=True))
    last_filters_refresh_at = Column(TIMESTAMP(timezone=True))
    last_fees_refresh_at    = Column(TIMESTAMP(timezone=True))
    last_limits_refresh_at  = Column(TIMESTAMP(timezone=True))

    status     = Column(Text)
    status_msg = Column(Text)

    features = Column(JSONB, server_default=text("'{}'::jsonb"))
    extra    = Column(JSONB, server_default=text("'{}'::jsonb"))

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    # 🔗 Relationships
    credentials = relationship("ExchangeCredential", back_populates="exchange", cascade="all, delete-orphan")
    symbols     = relationship("ExchangeSymbol", back_populates="exchange", cascade="all, delete-orphan")
    limits      = relationship("ExchangeLimit", back_populates="exchange", cascade="all, delete-orphan")
    status_history = relationship("ExchangeStatusHistory", back_populates="exchange", cascade="all, delete-orphan")
    fees        = relationship("ExchangeFee", back_populates="exchange", cascade="all, delete-orphan")


class ExchangeCredential(Base):
    __tablename__ = "exchange_credentials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id", ondelete="CASCADE"), nullable=False)

    label      = Column(Text)
    is_service = Column(Boolean, nullable=False, server_default=text("true"))
    is_active  = Column(Boolean, nullable=False, server_default=text("true"))

    api_key        = Column(Text)
    api_secret     = Column(Text)
    api_passphrase = Column(Text)
    subaccount     = Column(Text)
    scopes         = Column(JSONB, server_default=text("'[]'::jsonb"))

    secret_ref = Column(Text)
    vault_path = Column(Text)

    valid_from = Column(TIMESTAMP(timezone=True))
    valid_to   = Column(TIMESTAMP(timezone=True))

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    exchange = relationship("Exchange", back_populates="credentials")


class ExchangeSymbol(Base):
    __tablename__ = "exchange_symbols"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id", ondelete="CASCADE"))
    symbol_id   = Column(Text, nullable=False)
    symbol      = Column(Text, nullable=False)

    base_asset  = Column(Text, nullable=False)
    quote_asset = Column(Text, nullable=False)
    status      = Column(Text)
    type        = Column(Text, server_default="spot")

    base_precision  = Column(Integer)
    quote_precision = Column(Integer)
    step_size   = Column(Numeric)
    tick_size   = Column(Numeric)
    min_qty     = Column(Numeric)
    max_qty     = Column(Numeric)
    min_notional = Column(Numeric)
    max_notional = Column(Numeric)

    filters   = Column(JSONB, server_default="{}")
    is_active = Column(Boolean, nullable=False, server_default="true")

    fetched_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    exchange = relationship("Exchange", back_populates="symbols")
    fees     = relationship("ExchangeFee", back_populates="symbol", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("exchange_id", "symbol_id", name="uq_exchange_symbol"),)


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
