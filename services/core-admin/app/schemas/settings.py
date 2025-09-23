from pydantic import BaseModel

class SettingBase(BaseModel):
    key: str
    value: str
    enabled: bool = True

class SettingCreate(SettingBase):
    pass

class SettingUpdate(SettingBase):
    pass

class SettingOut(SettingBase):
    id: int

    class Config:
        orm_mode = True
