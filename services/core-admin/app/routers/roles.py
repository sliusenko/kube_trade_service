from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.deps.db import get_session
from app.models.auth import Role
from app.schemas.roles import RoleCreate, RoleUpdate, RoleOut

router = APIRouter(prefix="/roles", tags=["Roles"])


# ----------------------------------------------------------------
# List roles
# ----------------------------------------------------------------
@router.get("/", response_model=List[RoleOut])
async def list_roles(
    limit: int = Query(200, le=1000),
    session: AsyncSession = Depends(get_session),
):
    res = await session.execute(select(Role).limit(limit))
    return res.scalars().all()


# ----------------------------------------------------------------
# Create role
# ----------------------------------------------------------------
@router.post("/", response_model=RoleOut)
async def create_role(data: RoleCreate, session: AsyncSession = Depends(get_session)):
    role = Role(**data.dict())
    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role


# ----------------------------------------------------------------
# Update role
# ----------------------------------------------------------------
@router.put("/{role_name}", response_model=RoleOut)
async def update_role(role_name: str, data: RoleUpdate, session: AsyncSession = Depends(get_session)):
    role = await session.get(Role, role_name)  # PK = name
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(role, k, v)

    await session.commit()
    await session.refresh(role)
    return role


# ----------------------------------------------------------------
# Delete role
# ----------------------------------------------------------------
@router.delete("/{role_name}")
async def delete_role(role_name: str, session: AsyncSession = Depends(get_session)):
    role = await session.get(Role, role_name)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    await session.delete(role)
    await session.commit()
    return {"ok": True}
