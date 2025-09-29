from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from common.deps.db import get_session
from common.models.auth import Permission
from common.schemas.permissions import PermissionCreate, PermissionUpdate, PermissionOut

router = APIRouter(prefix="/permissions", tags=["Permissions"])


# ----------------------------------------------------------------
# Create Permission
# ----------------------------------------------------------------
@router.post("/", response_model=PermissionOut)
async def create_permission(
    payload: PermissionCreate,
    session: AsyncSession = Depends(get_session),
):
    permission = Permission(**payload.dict())
    session.add(permission)
    await session.commit()
    await session.refresh(permission)
    return permission


# ----------------------------------------------------------------
# List Permissions
# ----------------------------------------------------------------
@router.get("/", response_model=List[PermissionOut])
async def list_permissions(
    limit: int = Query(200, le=1000),
    session: AsyncSession = Depends(get_session),
):
    res = await session.execute(select(Permission).limit(limit))
    return res.scalars().all()


# ----------------------------------------------------------------
# Get Permission by name
# ----------------------------------------------------------------
@router.get("/{permission_name}", response_model=PermissionOut)
async def get_permission(
    permission_name: str,
    session: AsyncSession = Depends(get_session),
):
    permission = await session.get(Permission, permission_name)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


# ----------------------------------------------------------------
# Update Permission
# ----------------------------------------------------------------
@router.put("/{permission_name}", response_model=PermissionOut)
async def update_permission(
    permission_name: str,
    payload: PermissionUpdate,
    session: AsyncSession = Depends(get_session),
):
    permission = await session.get(Permission, permission_name)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(permission, k, v)

    await session.commit()
    await session.refresh(permission)
    return permission


# ----------------------------------------------------------------
# Delete Permission
# ----------------------------------------------------------------
@router.delete("/{permission_name}")
async def delete_permission(
    permission_name: str,
    session: AsyncSession = Depends(get_session),
):
    permission = await session.get(Permission, permission_name)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    await session.delete(permission)
    await session.commit()
    return {"ok": True}
