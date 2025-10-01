from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, SecretStr, ConfigDict

# -----------------------------
# User
# -----------------------------
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=64)   # Required username, must be 3–64 characters
    email: EmailStr                                     # Required, must be a valid email address
    role: Optional[str] = "viewer"                      # Role name (string), defaults to "viewer" if not provided
    is_active: bool = True                              # Active flag, defaults to True
class UserCreate(UserBase):
    # Accept plain password in create request, store hash in DB
    password: SecretStr = Field(min_length=8, max_length=128)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=64)  # Optional, must be 3–64 characters if provided
    email: Optional[EmailStr] = None                                   # Optional, must be valid email if provided
    role: Optional[str] = None                                         # Optional, can update user role
    is_active: Optional[bool] = None                                   # Optional, update active flag
    new_password: Optional[SecretStr] = Field(                         # Optional, new password (8–128 characters)
        default=None, min_length=8, max_length=128
    )
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)     # Enable ORM mode for SQLAlchemy models

    user_id: UUID                                       # UUID of the user
    username: str                                       # Username string
    email: EmailStr                                     # Valid email
    role: Optional[str] = "viewer"                      # Role string, defaults to "viewer" if missing
    created_at: datetime                                # Creation timestamp
    is_active: bool                                     # Active flag

# -----------------------------
# Role
# -----------------------------
class RoleBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)      # Role name, must be 2–50 characters
    description: Optional[str] = None                   # Optional description
class RoleCreate(RoleBase):
    pass                                                # Inherits all fields from RoleBase
class RoleUpdate(BaseModel):
    description: Optional[str] = None                   # Optional description for updating role
class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)     # Enable ORM mode for SQLAlchemy models

    name: str                                           # Role name
    description: Optional[str] = None                   # Optional description

# -----------------------------
# Permission
# -----------------------------
class PermissionBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)      # Permission name, must be 2–50 characters
    description: Optional[str] = None                   # Optional description
class PermissionCreate(PermissionBase):
    pass                                                # Inherits all fields from PermissionBase
class PermissionUpdate(BaseModel):
    description: Optional[str] = None                   # Optional description for updating permission
class PermissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)     # Enable ORM mode for SQLAlchemy models

    name: str                                           # Permission name
    description: Optional[str] = None                   # Optional description

# -----------------------------
# Role_Permission
# -----------------------------
class RolePermissionBase(BaseModel):
    role_name: str                                      # Role name (must exist in roles table)
    permission_name: str                                # Permission name (must exist in permissions table)
class RolePermissionCreate(RolePermissionBase):
    pass                                                # Inherits all fields from RolePermissionBase
class RolePermissionOut(RolePermissionBase):
    model_config = ConfigDict(from_attributes=True)     # Enable ORM mode for SQLAlchemy models
