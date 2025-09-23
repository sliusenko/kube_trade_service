from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.deps.db import get_session
from app.models.settings import Setting
from app.schemas.settings import SettingCreate, SettingUpdate, SettingOut

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/", response_model=list[SettingOut])
async def list_settings(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Setting))
    return result.scalars().all()

@router.post("/", response_model=SettingOut)
async def create_setting(setting: SettingCreate, session: AsyncSession = Depends(get_session)):
    db_setting = Setting(**setting.dict())
    session.add(db_setting)
    await session.commit()
    await session.refresh(db_setting)
    return db_setting

@router.put("/{setting_id}", response_model=SettingOut)
async def update_setting(setting_id: int, setting: SettingUpdate, session: AsyncSession = Depends(get_session)):
    db_setting = await session.get(Setting, setting_id)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    for k, v in setting.dict().items():
        setattr(db_setting, k, v)
    await session.commit()
    await session.refresh(db_setting)
    return db_setting

@router.delete("/{setting_id}")
async def delete_setting(setting_id: int, session: AsyncSession = Depends(get_session)):
    db_setting = await session.get(Setting, setting_id)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    await session.delete(db_setting)
    await session.commit()
    return {"ok": True}
