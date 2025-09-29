from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.deps.db import get_session
from common.models.auth import Role, RolePermission, Permission
from common.schemas.role_permissions import RolePermissionCreate, RolePermissionOut

router = APIRouter(prefix="/role-permissions", tags=["RolePermissions"])


# ----------------------------------------------------------------
# List all Role-Permission bindings
# ----------------------------------------------------------------
@router.get("/", response_model=List[RolePermissionOut])
async def list_role_permissions(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(RolePermission))
    return res.scalars().all()


# ----------------------------------------------------------------
# Add Role-Permission binding
# ----------------------------------------------------------------
@router.post("/", response_model=RolePermissionOut)
async def add_role_permission(
    payload: RolePermissionCreate,
    session: AsyncSession = Depends(get_session),
):
    # перевірка існування ролі
    if not await session.get(Role, payload.role_name):
        raise HTTPException(status_code=404, detail="Role not found")

    # перевірка існування пермішена
    if not await session.get(Permission, payload.permission_name):
        raise HTTPException(status_code=404, detail="Permission not found")

    role_permission = RolePermission(**payload.dict())
    session.add(role_permission)

    try:
        await session.commit()
        # ⚠️ refresh() не потрібен через composite PK
        return role_permission
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Already bound")


# ----------------------------------------------------------------
# Remove Role-Permission binding
# ----------------------------------------------------------------
@router.delete("/{role_name}/{permission_name}")
async def remove_role_permission(
    role_name: str,
    permission_name: str,
    session: AsyncSession = Depends(get_session),
):
    res = await session.execute(
        select(RolePermission).where(
            RolePermission.role_name == role_name,
            RolePermission.permission_name == permission_name,
        )
    )
    role_permission = res.scalar_one_or_none()
    if not role_permission:
        raise HTTPException(
            status_code=404,
            detail=f"Bind not found for role='{role_name}', permission='{permission_name}'",
        )

    await session.delete(role_permission)
    await session.commit()
    return {"ok": True}
