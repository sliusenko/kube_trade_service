from pydantic import BaseModel, EmailStr
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

# Users
class UserSchema(BaseModel):
    id: Optional[str] = None
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email address")
    role: Optional[str] = Field(default=None, description="Role name")
    is_active: bool = Field(default=True, description="Whether the user is active")

    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
# 🔹 Базове — спільні поля
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

# 🔹 Для створення
class UserCreate(UserBase):
    password: str
    role: str = "user"

# 🔹 Для відповіді (читаємо з БД)
class UserOut(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # у Pydantic v2

# 🔹 Для оновлення
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None

# Roles
class RoleSchema(BaseModel):
    name: str = Field(..., description="Role name")
    description: Optional[str] = Field(default=None, description="Role description")

    class Config:
        from_attributes = True
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
class PermissionSchema(BaseModel):
    name: str = Field(..., description="Permission name")
    description: Optional[str] = Field(default=None, description="Permission description")

    class Config:
        from_attributes = True
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
class RolePermissionSchema(BaseModel):
    role_name: str = Field(..., description="Role name")
    permission_name: str = Field(..., description="Permission name")

    class Config:
        from_attributes = True
class RolePermissionBase(BaseModel):
    role_name: str
    permission_name: str
class RolePermissionCreate(RolePermissionBase): pass
class RolePermissionOut(RolePermissionBase):
    role_name: str
    permission_name: str
    class Config:
        from_attributes = True
