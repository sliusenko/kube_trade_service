from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

# -----------------------------
# User
# -----------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]
    is_active: Optional[bool]


class UserOut(UserBase):
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
