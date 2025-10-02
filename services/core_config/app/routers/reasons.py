from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.deps.db import get_session
from common.models.config import ReasonCode
from common.schemas.config import ReasonCodeCreate, ReasonCodeUpdate, ReasonCodeRead
from common.crud.base import CRUDBase

router = APIRouter(prefix="/reasons", tags=["reasons"])

crud = CRUDBase[ReasonCode, ReasonCodeCreate, ReasonCodeUpdate](ReasonCode)


@router.get("/", response_model=list[ReasonCodeRead])
async def list_reasons(db: AsyncSession = Depends(get_session)):
    return await crud.get_all(db)


@router.get("/{code}", response_model=ReasonCodeRead)
async def get_reason(code: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(ReasonCode, code)
    if not obj:
        raise HTTPException(status_code=404, detail="Reason not found")
    return obj


@router.post("/", response_model=ReasonCodeRead)
async def create_reason(item: ReasonCodeCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create(db, item)


@router.put("/{code}", response_model=ReasonCodeRead)
async def update_reason(code: str, item: ReasonCodeUpdate, db: AsyncSession = Depends(get_session)):
    obj = await db.get(ReasonCode, code)
    if not obj:
        raise HTTPException(status_code=404, detail="Reason not found")
    return await crud.update(db, obj, item)


@router.delete("/{code}")
async def delete_reason(code: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(ReasonCode, code)
    if not obj:
        raise HTTPException(status_code=404, detail="Reason not found")
    return await crud.delete(db, obj)
