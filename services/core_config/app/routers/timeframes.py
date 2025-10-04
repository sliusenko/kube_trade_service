from typing import Optional
from uuid import UUID
from fastapi import Query, APIRouter, Depends, HTTPException
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
async def list_timeframes(
    exchange_id: Optional[UUID] = Query(None, description="Filter by exchange_id"),
    db: AsyncSession = Depends(get_session),
):
    query = select(Timeframe)
    if exchange_id:
        query = query.where(Timeframe.exchange_id == exchange_id)

    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=TimeframeRead)
async def create_timeframe(
    item: TimeframeCreate,
    db: AsyncSession = Depends(get_session),
    exchange_id: UUID = Query(...),
):

    result = await db.execute(
        select(Timeframe)
        .where(Timeframe.code == item.code)
        .where(Timeframe.exchange_id == exchange_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Timeframe already exists")

    item_dict = item.dict()
    item_dict["exchange_id"] = exchange_id
    item = TimeframeCreate(**item_dict)

    return await crud.create(db, item)

@router.get("/{code}", response_model=TimeframeRead)
async def get_timeframe(code: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Timeframe).where(Timeframe.code == code))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Timeframe not found")
    return obj

@router.put("/{code}", response_model=TimeframeRead)
async def update_timeframe(
    code: str,
    item: TimeframeUpdate,
    db: AsyncSession = Depends(get_session),
    exchange_id: UUID = Query(...),
):
    result = await db.execute(
        select(Timeframe)
        .where(Timeframe.code == code)
        .where(Timeframe.exchange_id == exchange_id)
    )
    obj = result.scalar_one_or_none()

    if not obj:
        raise HTTPException(status_code=404, detail="Timeframe not found")

    return await crud.update(db, obj, item)

@router.delete("/{code}")
async def delete_timeframe(
    code: str,
    db: AsyncSession = Depends(get_session),
    exchange_id: UUID = Query(...),
):
    result = await db.execute(
        select(Timeframe)
        .where(Timeframe.code == code)
        .where(Timeframe.exchange_id == exchange_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Timeframe not found")

    return await crud.delete(db, obj)