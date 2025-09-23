from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Users
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
class UserOut(UserBase):
    user_id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True

# 🔹 Для оновлення
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
    id: int
    class Config:
        from_attributes = True

# Permissions
class PermissionBase(BaseModel):
    code: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase): pass
class PermissionUpdate(PermissionBase): pass

class PermissionOut(PermissionBase):
    id: int
    class Config:
        from_attributes = True

# RolePermission (binding)
class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int
    user_id: Optional[int] = None

class RolePermissionCreate(RolePermissionBase): pass

class RolePermissionOut(RolePermissionBase):
    id: int
    class Config:
        from_attributes = True
