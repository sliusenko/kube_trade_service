from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, Dict, List

# -----------------------------
# Exchange
# -----------------------------
class ExchangeBase(BaseModel):
    code: str
    name: str
    kind: Optional[str] = "spot"
    environment: Optional[str] = "prod"
    base_url_public: Optional[str] = None
    base_url_private: Optional[str] = None
    ws_public_url: Optional[str] = None
    ws_private_url: Optional[str] = None
    data_feed_url: Optional[str] = None
    fetch_symbols_interval_min: Optional[int] = 60
    fetch_filters_interval_min: Optional[int] = 1440
    fetch_limits_interval_min: Optional[int] = 1440
    is_active: Optional[bool] = True
class ExchangeCreate(ExchangeBase):
    pass
class ExchangeUpdate(BaseModel):
    name: Optional[str]
    kind: Optional[str]
    environment: Optional[str]
    base_url_public: Optional[str]
    base_url_private: Optional[str]
    ws_public_url: Optional[str]
    ws_private_url: Optional[str]
    data_feed_url: Optional[str]
    fetch_symbols_interval_min: Optional[int]
    fetch_filters_interval_min: Optional[int]
    fetch_limits_interval_min: Optional[int]
    is_active: Optional[bool]
class ExchangeRead(ExchangeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class ExchangeSchema(BaseModel):
    id: Optional[str] = None
    code: str
    name: str
    kind: str = Field(default="spot", description="Exchange type")
    environment: str = Field(default="prod", description="Environment")

    base_url_public: Optional[str] = None
    base_url_private: Optional[str] = None
    ws_public_url: Optional[str] = None
    ws_private_url: Optional[str] = None
    data_feed_url: Optional[str] = None

    fetch_symbols_interval_min: int = 60
    fetch_filters_interval_min: int = 1440
    fetch_limits_interval_min: int = 1440

    rate_limit_per_min: Optional[int] = None
    recv_window_ms: int = 5000
    request_timeout_ms: int = 10000

    is_active: bool = True

    status: Optional[str] = None
    status_msg: Optional[str] = None

    features: Dict = {}
    extra: Dict = {}

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# -----------------------------
# ExchangeCredential
# -----------------------------
class ExchangeCredentialBase(BaseModel):
    label: Optional[str] = None
    is_service: Optional[bool] = True
    is_active: Optional[bool] = True
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    api_passphrase: Optional[str] = None
    subaccount: Optional[str] = None
class ExchangeCredentialCreate(ExchangeCredentialBase):
    pass
class ExchangeCredentialRead(ExchangeCredentialBase):
    id: UUID
    exchange_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# -----------------------------
# ExchangeSymbol (read-only)
# -----------------------------
class ExchangeSymbolRead(BaseModel):
    id: int
    exchange_id: UUID
    symbol: str
    base_asset: str
    quote_asset: str
    status: Optional[str]
    type: Optional[str]
    step_size: Optional[float]
    tick_size: Optional[float]
    min_qty: Optional[float]
    max_qty: Optional[float]
    min_notional: Optional[float]
    max_notional: Optional[float]
    filters: dict
    is_active: bool
    fetched_at: datetime

    class Config:
        from_attributes = True

# -----------------------------
# ExchangeLimit (read-only)
# -----------------------------
class ExchangeLimitRead(BaseModel):
    id: int
    exchange_id: UUID
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
    exchange_id: UUID
    event: str
    status: str
    message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
