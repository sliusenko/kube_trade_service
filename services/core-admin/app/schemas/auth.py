from pydantic import BaseModel, EmailStr
from typing import Optional

# Users
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase): pass
class UserUpdate(UserBase): pass

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

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
