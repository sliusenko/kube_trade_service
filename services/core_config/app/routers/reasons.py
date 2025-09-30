from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from common.models.config import ReasonCode
from common.schemas.config import ReasonCodeSchema
from common.deps.db import get_session

router = APIRouter(prefix="/reasons", tags=["reasons"])


@router.get("/", response_model=list[ReasonCodeSchema])
async def list_reasons(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(ReasonCode))
    return res.scalars().all()


@router.get("/{code}", response_model=ReasonCodeSchema)
async def get_reason(code: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(ReasonCode, code)
    if not obj:
        raise HTTPException(404, "Reason not found")
    return obj


@router.post("/", response_model=ReasonCodeSchema)
async def create_reason(item: ReasonCodeSchema, db: AsyncSession = Depends(get_session)):
    obj = ReasonCode(**item.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{code}", response_model=ReasonCodeSchema)
async def update_reason(code: str, item: ReasonCodeSchema, db: AsyncSession = Depends(get_session)):
    obj = await db.get(ReasonCode, code)
    if not obj:
        raise HTTPException(404, "Reason not found")
    for key, value in item.dict().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{code}")
async def delete_reason(code: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(ReasonCode, code)
    if not obj:
        raise HTTPException(404, "Reason not found")
    await db.delete(obj)
    await db.commit()
    return {"status": "deleted"}
