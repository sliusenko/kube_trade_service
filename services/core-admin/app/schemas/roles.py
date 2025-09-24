from pydantic import BaseModel
from typing import Optional


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
