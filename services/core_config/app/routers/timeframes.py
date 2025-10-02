from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from common.deps.db import get_session
from common.models.config import Timeframe
from common.schemas.config import TimeframeCreate, TimeframeUpdate, TimeframeRead
from common.crud.base import CRUDBase

router = APIRouter(prefix="/timeframes", tags=["timeframes"])

# Базовий CRUD
crud = CRUDBase[Timeframe, TimeframeCreate, TimeframeUpdate](Timeframe)


@router.get("/", response_model=list[TimeframeRead])
async def list_timeframes(db: AsyncSession = Depends(get_session)):
    return await crud.get_all(db)

@router.post("/", response_model=TimeframeRead)
async def create_timeframe(item: TimeframeCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create(db, item)

@router.get("/{code}", response_model=TimeframeRead)
async def get_timeframe(code: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Timeframe).where(Timeframe.code == code))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Timeframe not found")
    return obj

@router.put("/{code}", response_model=TimeframeRead)
async def update_timeframe(code: str, item: TimeframeUpdate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Timeframe).where(Timeframe.code == code))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Timeframe not found")
    return await crud.update(db, obj, item)

@router.delete("/{code}")
async def delete_timeframe(code: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Timeframe).where(Timeframe.code == code))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Timeframe not found")
    return await crud.delete(db, obj)
