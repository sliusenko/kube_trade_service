from pydantic import BaseModel
from typing import Optional


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
