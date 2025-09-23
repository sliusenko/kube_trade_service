from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.deps.db import get_session
from app.models.auth import Permission
from app.schemas.auth import PermissionCreate, PermissionUpdate, PermissionOut

router = APIRouter(prefix="/permissions", tags=["Permissions"])

# Створити Permission
@router.post("/", response_model=PermissionOut)
async def create_permission(
    data: PermissionCreate,
    session: AsyncSession = Depends(get_session),
):
    obj = Permission(**data.dict())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


# Отримати список
@router.get("/", response_model=list[PermissionOut])
async def list_permissions(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Permission))
    return res.scalars().all()


# Отримати одне Permission
@router.get("/{permission_name}", response_model=PermissionOut)
async def get_permission(
    permission_name: str,
    session: AsyncSession = Depends(get_session),
):
    obj = await session.get(Permission, permission_name)
    if not obj:
        raise HTTPException(status_code=404, detail="Permission not found")
    return obj


# Оновити Permission
@router.put("/{permission_name}", response_model=PermissionOut)
async def update_permission(
    permission_name: str,
    data: PermissionUpdate,
    session: AsyncSession = Depends(get_session),
):
    obj = await session.get(Permission, permission_name)
    if not obj:
        raise HTTPException(status_code=404, detail="Permission not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    await session.commit()
    await session.refresh(obj)
    return obj


# Видалити Permission
@router.delete("/{permission_name}")
async def delete_permission(
    permission_name: str,
    session: AsyncSession = Depends(get_session),
):
    obj = await session.get(Permission, permission_name)
    if not obj:
        raise HTTPException(status_code=404, detail="Permission not found")
    await session.delete(obj)
    await session.commit()
    return {"ok": True}
