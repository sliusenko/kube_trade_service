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

# -----------------------------
# Permission
# -----------------------------
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
class PermissionCreate(PermissionBase):
    pass
class PermissionUpdate(BaseModel):
    description: Optional[str]
class PermissionOut(PermissionBase):
    class Config:
        from_attributes = True

# -----------------------------
# Role
# -----------------------------
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
class RoleCreate(RoleBase):
    pass
class RoleUpdate(BaseModel):
    description: Optional[str]
class RoleOut(RoleBase):
    class Config:
        from_attributes = True
        
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
