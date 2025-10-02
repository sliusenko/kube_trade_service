from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from common.deps.db import get_session
from common.models.config import Setting
from common.schemas.config import SettingCreate, SettingRead, SettingUpdate
from common.crud.base import CRUDBase

router = APIRouter(prefix="/settings", tags=["settings"])

crud = CRUDBase[Setting, SettingCreate, SettingUpdate](Setting)

@router.get("/", response_model=list[SettingRead])
async def list_all_settings(db: AsyncSession = Depends(get_session)):
    """Отримати всі налаштування для всіх сервісів"""
    result = await db.execute(select(Setting))
    return result.scalars().all()


@router.get("/{service_name}", response_model=list[SettingRead])
async def list_settings(service_name: str, db: AsyncSession = Depends(get_session)):
    """Отримати всі налаштування конкретного сервісу"""
    result = await db.execute(select(Setting).where(Setting.service_name == service_name))
    return result.scalars().all()


@router.post("/", response_model=SettingRead)
async def create_setting(payload: SettingCreate, db: AsyncSession = Depends(get_session)):
    """Створити нове налаштування"""
    return await crud.create(db, payload)


@router.put("/{setting_id}", response_model=SettingRead)
async def update_setting(setting_id: str, payload: SettingUpdate, db: AsyncSession = Depends(get_session)):
    """Оновити значення налаштування"""
    obj = await db.get(Setting, setting_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Setting not found")
    return await crud.update(db, obj, payload)


@router.delete("/{setting_id}")
async def delete_setting(setting_id: str, db: AsyncSession = Depends(get_session)):
    """Видалити налаштування"""
    obj = await db.get(Setting, setting_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Setting not found")
    return await crud.delete(db, obj)
