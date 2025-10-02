from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.deps.db import get_session
from common.models.config import TradeCondition
from common.schemas.config import (
    TradeConditionCreate, TradeConditionUpdate, TradeConditionRead
)
from common.crud.base import CRUDBase

router = APIRouter(prefix="/trade-conditions", tags=["trade_conditions"])

crud = CRUDBase[TradeCondition, TradeConditionCreate, TradeConditionUpdate](TradeCondition)


@router.get("/", response_model=list[TradeConditionRead])
async def list_trade_conditions(db: AsyncSession = Depends(get_session)):
    return await crud.get_all(db)


@router.get("/{condition_id}", response_model=TradeConditionRead)
async def get_trade_condition(condition_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeCondition, condition_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TradeCondition not found")
    return obj


@router.post("/", response_model=TradeConditionRead)
async def create_trade_condition(item: TradeConditionCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create(db, item)


@router.put("/{condition_id}", response_model=TradeConditionRead)
async def update_trade_condition(condition_id: int, item: TradeConditionUpdate, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeCondition, condition_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TradeCondition not found")
    return await crud.update(db, obj, item)


@router.delete("/{condition_id}")
async def delete_trade_condition(condition_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(TradeCondition, condition_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TradeCondition not found")
    return await crud.delete(db, obj)
