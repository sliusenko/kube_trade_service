from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, SecretStr, ConfigDict

# -----------------------------
# User
# -----------------------------
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    role: Optional[str] = None
    is_active: bool = True
class UserCreate(UserBase):
    # приймаємо пароль у create, а в БД зберігаємо hash
    password: SecretStr = Field(min_length=8, max_length=128)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=64)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    new_password: Optional[SecretStr] = Field(default=None, min_length=8, max_length=128)
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    username: str
    email: EmailStr
    role: Optional[str] = None
    created_at: datetime
    is_active: bool

# -----------------------------
# Role
# -----------------------------
class RoleBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: Optional[str] = None
class RoleCreate(RoleBase):
    pass
class RoleUpdate(BaseModel):
    description: Optional[str] = None
class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None

# -----------------------------
# Permission
# -----------------------------
class PermissionBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: Optional[str] = None
class PermissionCreate(PermissionBase):
    pass
class PermissionUpdate(BaseModel):
    description: Optional[str] = None
class PermissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None

# -----------------------------
# Role_Permission
# -----------------------------
class RolePermissionBase(BaseModel):
    role_name: str
    permission_name: str
class RolePermissionCreate(RolePermissionBase):
    pass
class RolePermissionOut(RolePermissionBase):
    class Config:
        from_attributes = True
