import uuid
from sqlalchemy import Column, Text, Integer, Boolean, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB, BIGINT
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Exchange(Base):
    __tablename__ = "exchanges"
    id = Column(UUID(as_uuid=True), primary_key=True)
    code = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    refresh_interval = Column(Integer, server_default="3600")  # сек
    credentials = relationship("ExchangeCredential", back_populates="exchange", cascade="all, delete-orphan")
    symbols = relationship("ExchangeSymbol", back_populates="exchange", cascade="all, delete-orphan")
    limits = relationship("ExchangeLimit", back_populates="exchange", cascade="all, delete-orphan")
    status_history = relationship("ExchangeStatusHistory", back_populates="exchange", cascade="all, delete-orphan")
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
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id", ondelete="CASCADE"))
    symbol = Column(Text, nullable=False)
    base_asset = Column(Text)
    quote_asset = Column(Text)
    step_size = Column(Numeric)
    tick_size = Column(Numeric)
    min_qty = Column(Numeric)
    max_qty = Column(Numeric)
    filters = Column(JSONB, server_default="{}")
    is_active = Column(Boolean, nullable=False, server_default="true")
    fetched_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    exchange = relationship("Exchange", back_populates="symbols")
class ExchangeLimit(Base):
    __tablename__ = "exchange_limits"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id", ondelete="CASCADE"))
    limit_type = Column(Text, nullable=False)
    interval_unit = Column(Text, nullable=False)
    interval_num = Column(Integer, nullable=False)
    limit = Column(Integer, nullable=False)
    raw_json = Column(JSONB, server_default="{}")
    fetched_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    exchange = relationship("Exchange", back_populates="limits")
class ExchangeStatusHistory(Base):
    __tablename__ = "exchange_status_history"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id", ondelete="CASCADE"))
    event = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    message = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
