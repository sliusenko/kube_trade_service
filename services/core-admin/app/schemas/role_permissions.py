from pydantic import BaseModel

class RolePermissionBase(BaseModel):
    role_name: str
    permission_name: str

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionOut(RolePermissionBase):
    class Config:
        from_attributes = True
