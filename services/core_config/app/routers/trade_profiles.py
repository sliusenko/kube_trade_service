from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from common.models.config import TradeProfile
from common.schemas.config import TradeProfileSchema
from common.deps.db import get_session

router = APIRouter(prefix="/trade-profiles", tags=["trade_profiles"])


@router.get("/", response_model=list[TradeProfileSchema])
async def list_trade_profiles(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(TradeProfile))
    return res.scalars().all()


@router.get("/{profile_id}", response_model=TradeProfileSchema)
async def get_trade_profile(profile_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeProfile, profile_id)
    if not obj:
        raise HTTPException(404, "TradeProfile not found")
    return obj


@router.post("/", response_model=TradeProfileSchema)
async def create_trade_profile(item: TradeProfileSchema, db: AsyncSession = Depends(get_session)):
    obj = TradeProfile(**item.dict(exclude={"id"}))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{profile_id}", response_model=TradeProfileSchema)
async def update_trade_profile(profile_id: int, item: TradeProfileSchema, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeProfile, profile_id)
    if not obj:
        raise HTTPException(404, "TradeProfile not found")
    for key, value in item.dict(exclude={"id"}).items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{profile_id}")
async def delete_trade_profile(profile_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeProfile, profile_id)
    if not obj:
        raise HTTPException(404, "TradeProfile not found")
    await db.delete(obj)
    await db.commit()
    return {"status": "deleted"}
