from datetime import datetime
import uuid
from typing import Optional, List, Literal, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import (
    Column, BigInteger, Numeric, Text, Boolean, Integer, SmallInteger,
    ForeignKey, TIMESTAMP, UniqueConstraint, text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from common.models.base import Base

# -----------------------------
# Exchange
# -----------------------------
class ExchangeBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=20)
    name: str
    kind: str = "spot"
    environment: str = "prod"

    base_url_public: Optional[str] = None
    base_url_private: Optional[str] = None
    ws_public_url: Optional[str] = None
    ws_private_url: Optional[str] = None
    data_feed_url: Optional[str] = None

    fetch_symbols_interval_min: int = 60
    fetch_filters_interval_min: int = 1440
    fetch_limits_interval_min: int = 1440
    fetch_fees_interval_min: int = 1440

    rate_limit_per_min: Optional[int] = None
    recv_window_ms: int = 5000
    request_timeout_ms: int = 10000

    is_active: bool = True

    status: Optional[str] = None
    status_msg: Optional[str] = None

    features: Dict[str, Any] = {}
    extra: Dict[str, Any] = {}
class ExchangeCreate(ExchangeBase):
    pass
class ExchangeUpdate(BaseModel):
    name: Optional[str] = None
    kind: Optional[str] = None
    environment: Optional[str] = None
    base_url_public: Optional[str] = None
    base_url_private: Optional[str] = None
    ws_public_url: Optional[str] = None
    ws_private_url: Optional[str] = None
    data_feed_url: Optional[str] = None
    fetch_symbols_interval_min: Optional[int] = None
    fetch_filters_interval_min: Optional[int] = None
    fetch_limits_interval_min: Optional[int] = None
    fetch_fees_interval_min: Optional[int] = None
    rate_limit_per_min: Optional[int] = None
    recv_window_ms: Optional[int] = None
    request_timeout_ms: Optional[int] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None
    status_msg: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    extra: Optional[Dict[str, Any]] = None
class ExchangeOut(ExchangeBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    last_symbols_refresh_at: Optional[datetime] = None
    last_filters_refresh_at: Optional[datetime] = None
    last_fees_refresh_at: Optional[datetime] = None
    last_limits_refresh_at: Optional[datetime] = None

# -----------------------------
# ExchangeCredential
# -----------------------------
class ExchangeCredentialBase(BaseModel):
    exchange_id: UUID
    label: Optional[str] = None
    is_service: bool = True
    is_active: bool = True
    scopes: List[str] = []

    # reference to secret store instead of exposing secrets
    secret_ref: Optional[str] = None
    vault_path: Optional[str] = None

    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
class ExchangeCredentialCreate(ExchangeCredentialBase):
    # для створення — можна дозволити вводити ключі напряму
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    api_passphrase: Optional[str] = None
    subaccount: Optional[str] = None
class ExchangeCredentialUpdate(BaseModel):
    label: Optional[str] = None
    is_service: Optional[bool] = None
    is_active: Optional[bool] = None
    scopes: Optional[List[str]] = None
    secret_ref: Optional[str] = None
    vault_path: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

    # update secrets if rotated
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    api_passphrase: Optional[str] = None
    subaccount: Optional[str] = None
class ExchangeCredentialOut(ExchangeCredentialBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime

# -----------------------------
# ExchangeFee (read-only)
# -----------------------------
class ExchangeFeeRead(BaseModel):
    id: int
    exchange_id: uuid.UUID
    symbol_id: Optional[int]
    volume_threshold: float
    maker_fee: Optional[float]
    taker_fee: Optional[float]
    fetched_at: datetime

    class Config:
        from_attributes = True

# -----------------------------
# ExchangeLimit (read-only)
# -----------------------------
class ExchangeLimitRead(BaseModel):
    id: int
    exchange_id: uuid.UUID
    limit_type: str
    interval_unit: str
    interval_num: int
    limit: int
    raw_json: dict
    fetched_at: datetime

    class Config:
        from_attributes = True

# -----------------------------
# ExchangeStatusHistory (read-only)
# -----------------------------
class ExchangeStatusHistoryRead(BaseModel):
    id: int
    exchange_id: uuid.UUID
    event: str
    status: str
    message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
