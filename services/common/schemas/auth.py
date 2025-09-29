from pydantic import BaseModel, EmailStr
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

# Users
# 🔹 Базове — спільні поля
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
class UserCreate(UserBase):
    password: str
    role: str = "user"
class UserOut(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # у Pydantic v2
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None

# Roles
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
class RoleCreate(RoleBase): pass
class RoleUpdate(RoleBase): pass
class RoleOut(RoleBase):
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

# Permissions
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
class PermissionCreate(PermissionBase): pass
class PermissionUpdate(PermissionBase): pass
class PermissionOut(PermissionBase):
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

# RolePermission (binding)
class RolePermissionBase(BaseModel):
    role_name: str
    permission_name: str
class RolePermissionCreate(RolePermissionBase): pass
class RolePermissionOut(RolePermissionBase):
    role_name: str
    permission_name: str
    class Config:
        from_attributes = True
