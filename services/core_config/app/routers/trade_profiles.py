from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from common.deps.db import get_session
from common.models.config import TradeProfile
from common.schemas.config import TradeProfileCreate, TradeProfileUpdate, TradeProfileRead

router = APIRouter(prefix="/trade-profiles", tags=["trade_profiles"])


@router.get("/", response_model=list[TradeProfileRead])
async def list_trade_profiles(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(TradeProfile))
    return result.scalars().all()


@router.get("/{profile_id}", response_model=TradeProfileRead)
async def get_trade_profile(profile_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeProfile, profile_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TradeProfile not found")
    return obj


@router.post("/", response_model=TradeProfileRead)
async def create_trade_profile(item: TradeProfileCreate, db: AsyncSession = Depends(get_session)):
    # Перевірка на дублікат по name
    result = await db.execute(select(TradeProfile).where(TradeProfile.name == item.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail=f"Trade profile '{item.name}' already exists")

    obj = TradeProfile(**item.dict())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate profile name")


@router.put("/{profile_id}", response_model=TradeProfileRead)
async def update_trade_profile(profile_id: int, item: TradeProfileUpdate, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeProfile, profile_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TradeProfile not found")

    # Перевірка унікальності name при оновленні
    if item.name and item.name != obj.name:
        result = await db.execute(select(TradeProfile).where(TradeProfile.name == item.name))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail=f"Trade profile '{item.name}' already exists")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{profile_id}")
async def delete_trade_profile(profile_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeProfile, profile_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TradeProfile not found")

    await db.delete(obj)
    await db.commit()
    return {"status": "deleted"}
