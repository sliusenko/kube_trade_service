from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from typing import List

from app.deps.db import get_session
from app.models.auth import Role, RolePermission, Permission
from app.schemas.role_permissions import RolePermissionCreate, RolePermissionOut

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
    # перевіряємо, що роль існує
    if not await session.get(Role, payload.role_name):
        raise HTTPException(status_code=404, detail="Role not found")

    # перевіряємо, що пермішен існує
    if not await session.get(Permission, payload.permission_name):
        raise HTTPException(status_code=404, detail="Permission not found")

    try:
        result = await session.execute(
            insert(RolePermission)
            .values(**payload.dict())
            .returning(RolePermission)
        )
        await session.commit()
        return result.scalar_one()
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
