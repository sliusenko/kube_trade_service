from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Literal

# -----------------------------
# Exchange
# -----------------------------
class ExchangeBase(BaseModel):
    code: str = Field(..., description="Unique code for the exchange", example="BINANCE")
    name: str = Field(..., description="Full name of the exchange", example="Binance")

    # 👇 enum замість option1/2
    kind: Literal["spot", "futures", "margin"] = Field(
        default="spot", description="Exchange type"
    )
    environment: Literal["prod", "dev", "test"] = Field(
        default="prod", description="Environment"
    )

    base_url_public: Optional[str] = Field(
        None, description="Public REST API URL", example="https://api.binance.com"
    )
    base_url_private: Optional[str] = Field(
        None, description="Private REST API URL"
    )
    ws_public_url: Optional[str] = Field(
        None, description="Public WebSocket URL"
    )
    ws_private_url: Optional[str] = Field(
        None, description="Private WebSocket URL"
    )
    data_feed_url: Optional[str] = Field(
        None, description="Custom data feed URL"
    )

    fetch_symbols_interval_min: Optional[int] = Field(
        60, description="Interval (minutes) to fetch symbols"
    )
    fetch_filters_interval_min: Optional[int] = Field(
        1440, description="Interval (minutes) to fetch filters"
    )
    fetch_limits_interval_min: Optional[int] = Field(
        1440, description="Interval (minutes) to fetch limits"
    )

    is_active: Optional[bool] = Field(True, description="Is this exchange active?")
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

# -----------------------------
# ExchangeCredential
# -----------------------------
class ExchangeCredentialBase(BaseModel):
    label: Optional[str] = Field(
        None, description="Label for this credential", example="Main account"
    )
    is_service: Optional[bool] = Field(
        True, description="Used by service account?", example=True
    )
    is_active: Optional[bool] = Field(
        True, description="Is credential active?", example=True
    )

    api_key: Optional[str] = Field(
        None, description="API key", example="abcd1234",
        json_schema_extra={"format": "password"}  # 👈 підкаже зробити пароль
    )
    api_secret: Optional[str] = Field(
        None, description="API secret", example="secretXYZ",
        json_schema_extra={"format": "password"}
    )
    api_passphrase: Optional[str] = Field(
        None, description="API passphrase (if required)", example="myPass",
        json_schema_extra={"format": "password"}
    )
    subaccount: Optional[str] = Field(
        None, description="Subaccount name", example="trading-bot"
    )
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
# ExchangeFee (read-only)
# -----------------------------
class ExchangeFeeRead(BaseModel):
    id: int
    exchange_id: UUID
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
