from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from common.deps.db import get_db
from .models import Setting
from .schemas import SettingCreate, SettingRead, SettingUpdate

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("/{service_name}", response_model=list[SettingRead])
async def list_settings(service_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Setting).where(Setting.service_name == service_name))
    return result.scalars().all()

@router.post("/", response_model=SettingRead)
async def create_setting(payload: SettingCreate, db: AsyncSession = Depends(get_db)):
    obj = Setting(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

@router.put("/{setting_id}", response_model=SettingRead)
async def update_setting(setting_id: str, payload: SettingUpdate, db: AsyncSession = Depends(get_db)):
    setting = await db.get(Setting, setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting.value = payload.value
    setting.value_type = payload.value_type
    await db.commit()
    await db.refresh(setting)
    return setting

@router.delete("/{setting_id}")
async def delete_setting(setting_id: str, db: AsyncSession = Depends(get_db)):
    setting = await db.get(Setting, setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    await db.delete(setting)
    await db.commit()
    return {"status": "deleted"}
