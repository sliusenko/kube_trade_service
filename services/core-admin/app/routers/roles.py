from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from typing import List

from app.deps.db import get_session
from app.models.auth import Role, RolePermission, Permission
from app.schemas.auth import RoleCreate, RoleUpdate, RoleOut, RolePermissionCreate, RolePermissionOut

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RoleOut])
async def list_roles(limit: int = Query(200, le=1000), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Role).limit(limit))
    return res.scalars().all()

@router.post("/", response_model=RoleOut)
async def create_role(data: RoleCreate, session: AsyncSession = Depends(get_session)):
    obj = Role(**data.dict())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

@router.put("/{role_name}", response_model=RoleOut)
async def update_role(role_name: str, data: RoleUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Role, role_name)  # тут lookup по PK name
    if not obj:
        raise HTTPException(status_code=404, detail="Role not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    await session.commit()
    await session.refresh(obj)
    return obj

@router.delete("/{role_name}")
async def delete_role(role_name: str, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Role, role_name)
    if not obj:
        raise HTTPException(status_code=404, detail="Role not found")
    await session.delete(obj)
    await session.commit()
    return {"ok": True}

# --- прив'язка пермішенів до ролі / користувача
@router.post("/bind", response_model=RolePermissionOut, tags=["RolePermissions"])
async def bind_permission(payload: RolePermissionCreate, session: AsyncSession = Depends(get_session)):
    # перевірка наявності role/permission
    if not await session.get(Role, payload.role_name):
        raise HTTPException(status_code=404, detail="Role not found")
    if not await session.get(Permission, payload.permission_name):
        raise HTTPException(status_code=404, detail="Permission not found")

    stmt = insert(RolePermission).values(**payload.dict()).returning(RolePermission)
    res = await session.execute(stmt)
    await session.commit()
    return res.scalar_one()

@router.delete("/bind", tags=["RolePermissions"])
async def unbind_permission(payload: RolePermissionCreate, session: AsyncSession = Depends(get_session)):
    stmt = delete(RolePermission).where(
        RolePermission.role_name == payload.role_name,
        RolePermission.permission_name == payload.permission_name
    )
    res = await session.execute(stmt)
    await session.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Bind not found")
    return {"ok": True}
