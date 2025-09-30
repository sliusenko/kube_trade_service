from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from common.models.config import GroupIcon
from common.schemas.config import GroupIconSchema
from common.deps.db import get_session

router = APIRouter(prefix="/group-icons", tags=["group_icons"])


@router.get("/", response_model=list[GroupIconSchema])
async def list_group_icons(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(GroupIcon))
    return res.scalars().all()


@router.get("/{group_name}", response_model=GroupIconSchema)
async def get_group_icon(group_name: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(GroupIcon, group_name)
    if not obj:
        raise HTTPException(404, "GroupIcon not found")
    return obj


@router.post("/", response_model=GroupIconSchema)
async def create_group_icon(icon: GroupIconSchema, db: AsyncSession = Depends(get_session)):
    obj = GroupIcon(**icon.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{group_name}", response_model=GroupIconSchema)
async def update_group_icon(group_name: str, icon: GroupIconSchema, db: AsyncSession = Depends(get_session)):
    obj = await db.get(GroupIcon, group_name)
    if not obj:
        raise HTTPException(404, "GroupIcon not found")
    obj.icon = icon.icon
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{group_name}")
async def delete_group_icon(group_name: str, db: AsyncSession = Depends(get_session)):
    obj = await db.get(GroupIcon, group_name)
    if not obj:
        raise HTTPException(404, "GroupIcon not found")
    await db.delete(obj)
    await db.commit()
    return {"status": "deleted"}
