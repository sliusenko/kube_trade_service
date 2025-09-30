from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from common.models.config import TradeCondition
from common.schemas.config import TradeConditionSchema
from common.deps.db import get_session

router = APIRouter(prefix="/trade-conditions", tags=["trade_conditions"])


@router.get("/", response_model=list[TradeConditionSchema])
async def list_trade_conditions(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(TradeCondition))
    return res.scalars().all()


@router.get("/{condition_id}", response_model=TradeConditionSchema)
async def get_trade_condition(condition_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeCondition, condition_id)
    if not obj:
        raise HTTPException(404, "TradeCondition not found")
    return obj


@router.post("/", response_model=TradeConditionSchema)
async def create_trade_condition(item: TradeConditionSchema, db: AsyncSession = Depends(get_session)):
    obj = TradeCondition(**item.dict(exclude={"id"}))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{condition_id}", response_model=TradeConditionSchema)
async def update_trade_condition(condition_id: int, item: TradeConditionSchema, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeCondition, condition_id)
    if not obj:
        raise HTTPException(404, "TradeCondition not found")
    for key, value in item.dict(exclude={"id"}).items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{condition_id}")
async def delete_trade_condition(condition_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeCondition, condition_id)
    if not obj:
        raise HTTPException(404, "TradeCondition not found")
    await db.delete(obj)
    await db.commit()
    return {"status": "deleted"}
