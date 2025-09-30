from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from common.models.config import Timeframe
from common.schemas.config import TimeframeSchema
from common.deps.db import get_session

router = APIRouter(prefix="/timeframes", tags=["timeframes"])


@router.get("/", response_model=list[TimeframeSchema])
async def list_timeframes(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Timeframe))
    return res.scalars().all()


@router.get("/{code}", response_model=TimeframeSchema)
async def get_timeframe(code: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(Timeframe, code)
    if not obj:
        raise HTTPException(404, "Timeframe not found")
    return obj


@router.post("/", response_model=TimeframeSchema)
async def create_timeframe(item: TimeframeSchema, db: AsyncSession = Depends(get_session)):
    obj = Timeframe(**item.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{code}", response_model=TimeframeSchema)
async def update_timeframe(code: str, item: TimeframeSchema, db: AsyncSession = Depends(get_session)):
    obj = await db.get(Timeframe, code)
    if not obj:
        raise HTTPException(404, "Timeframe not found")
    for key, value in item.dict().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{code}")
async def delete_timeframe(code: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(Timeframe, code)
    if not obj:
        raise HTTPException(404, "Timeframe not found")
    await db.delete(obj)
    await db.commit()
    return {"status": "deleted"}
