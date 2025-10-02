from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

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

class CommandSchema(BaseModel):
    id: int
    command: str
    group_name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class GroupIconSchema(BaseModel):
    group_name: str
    icon: str

    class Config:
        from_attributes = True


class TimeframeSchema(BaseModel):
    code: str
    history_limit: Optional[int]
    min_len: Optional[int]
    hours: Optional[float]
    lookback: Optional[str]

    class Config:
        from_attributes = True


class ReasonCodeSchema(BaseModel):
    code: str
    description: str
    category: str

    class Config:
        from_attributes = True


class TradeProfileSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class TradeConditionSchema(BaseModel):
    id: int
    profile_id: int
    action: str
    condition_type: str
    param_1: Optional[float]
    param_2: Optional[float]
    priority: int

    class Config:
        from_attributes = True
