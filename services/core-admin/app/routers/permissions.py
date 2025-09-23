from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.deps.db import get_session
from app.models.auth import Permission
from app.schemas.auth import PermissionCreate, PermissionUpdate, PermissionOut

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.get("/", response_model=List[PermissionOut])
async def list_permissions(limit: int = Query(500, le=2000), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Permission).limit(limit))
    return res.scalars().all()

@router.post("/", response_model=PermissionOut)
async def create_permission(data: PermissionCreate, session: AsyncSession = Depends(get_session)):
    obj = Permission(**data.dict())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

@router.put("/{perm_id}", response_model=PermissionOut)
async def update_permission(perm_id: int, data: PermissionUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Permission, perm_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Permission not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    await session.commit()
    await session.refresh(obj)
    return obj

@router.delete("/{perm_id}")
async def delete_permission(perm_id: int, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Permission, perm_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Permission not found")
    await session.delete(obj)
    await session.commit()
    return {"ok": True}
