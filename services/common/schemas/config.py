from typing import Optional
from datetime import datetime, timedelta
from uuid import UUID
from pydantic import BaseModel, condecimal, field_validator
from decimal import Decimal

# -------- Settings --------
class SettingCreate(BaseModel):
    service_name: str
    key: str
    value: str
    value_type: str = "str"
class SettingUpdate(BaseModel):
    value: str
    value_type: str = "str"
class SettingRead(BaseModel):
    id: UUID
    service_name: str
    key: str
    value: str
    value_type: str
    updated_at: datetime
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True

# -------- Commands --------
class CommandCreate(BaseModel):
    command: str
    group_name: str
    description: Optional[str] = None
class CommandUpdate(BaseModel):
    command: Optional[str] = None
    group_name: Optional[str] = None
    description: Optional[str] = None
class CommandRead(BaseModel):
    id: int
    command: str
    group_name: str
    description: Optional[str]

    class Config:
        from_attributes = True

# -------- Group Icons --------
class GroupIconCreate(BaseModel):
    group_name: str
    icon: str
class GroupIconUpdate(BaseModel):
    icon: str
class GroupIconRead(BaseModel):
    group_name: str
    icon: str

    class Config:
        from_attributes = True

# -------- Timeframes --------
# -------- Timeframes --------
class TimeframeBase(BaseModel):
    code: str
    lookback: int | None = None   # секундами
    history_limit: int | None = None
    min_len: int | None = None
    hours: float | None = None
class TimeframeCreate(TimeframeBase):
    pass
class TimeframeUpdate(TimeframeBase):
    pass
class TimeframeRead(TimeframeBase):
    id: int

    class Config:
        from_attributes = True

# -------- Reasons --------
class ReasonCodeCreate(BaseModel):
    code: str              # PK, varchar
    description: str       # NOT NULL (text)
    category: str          # NOT NULL (varchar)
class ReasonCodeUpdate(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = None
class ReasonCodeRead(BaseModel):
    code: str
    description: str
    category: str

    class Config:
        from_attributes = True

# -------- Trade Profiles --------
class TradeProfileCreate(BaseModel):
    name: str                     # required, UNIQUE
    description: Optional[str] = None
class TradeProfileUpdate(BaseModel):
    name: Optional[str] = None     # дозволяє міняти тільки name або тільки description
    description: Optional[str] = None
class TradeProfileRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True

# -------- Trade Conditions --------
class TradeConditionCreate(BaseModel):
    profile_id: int                # FK -> trade_profiles.id
    action: str                    # varchar
    condition_type: str            # varchar
    param_1: Optional[float] = None  # numeric → float
    param_2: Optional[float] = None  # numeric → float
    priority: int                  # integer
class TradeConditionUpdate(BaseModel):
    action: Optional[str] = None
    condition_type: Optional[str] = None
    param_1: Optional[float] = None
    param_2: Optional[float] = None
    priority: Optional[int] = None
class TradeConditionRead(BaseModel):
    id: int
    profile_id: int
    action: str
    condition_type: str
    param_1: Optional[float]
    param_2: Optional[float]
    priority: int

    class Config:
        from_attributes = True
