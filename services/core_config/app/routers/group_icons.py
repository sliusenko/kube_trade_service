from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.deps.db import get_session
from common.models.config import GroupIcon
from common.schemas.config import GroupIconCreate, GroupIconUpdate, GroupIconRead
from common.crud.base import CRUDBase

router = APIRouter(prefix="/group-icons", tags=["group_icons"])

crud = CRUDBase[GroupIcon, GroupIconCreate, GroupIconUpdate](GroupIcon)


@router.get("/", response_model=list[GroupIconRead])
async def list_group_icons(db: AsyncSession = Depends(get_session)):
    return await crud.get_all(db)


@router.get("/{group_name}", response_model=GroupIconRead)
async def get_group_icon(group_name: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(GroupIcon, group_name)
    if not obj:
        raise HTTPException(status_code=404, detail="GroupIcon not found")
    return obj


@router.post("/", response_model=GroupIconRead)
async def create_group_icon(icon: GroupIconCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create(db, icon)


@router.put("/{group_name}", response_model=GroupIconRead)
async def update_group_icon(group_name: str, icon: GroupIconUpdate, db: AsyncSession = Depends(get_session)):
    obj = await db.get(GroupIcon, group_name)
    if not obj:
        raise HTTPException(status_code=404, detail="GroupIcon not found")
    return await crud.update(db, obj, icon)


@router.delete("/{group_name}")
async def delete_group_icon(group_name: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(GroupIcon, group_name)
    if not obj:
        raise HTTPException(status_code=404, detail="GroupIcon not found")
    return await crud.delete(db, obj)
