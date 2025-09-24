from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from app.deps.db import get_session
from app.models.auth import Role, RolePermission, Permission
from app.schemas.auth import RolePermissionCreate, RolePermissionOut

router = APIRouter(prefix="/roles", tags=["RolePermissions"]
)


# 1. Додавання пари Role - Permission
# --- прив'язка пермішенів до ролі / користувача
@router.post("/bind", response_model=RolePermissionOut, tags=["RolePermissions"])
async def add_role_permission(
    payload: RolePermissionCreate,
    session: AsyncSession = Depends(get_session),
):
    # перевірки існування РОЛІ/ПЕРМІШЕНА лишай, якщо хочеш жорстку цілісність
    if not await session.get(Role, payload.role_name):
        raise HTTPException(status_code=404, detail="Role not found")
    if not await session.get(Permission, payload.permission_name):
        raise HTTPException(status_code=404, detail="Permission not found")

    try:
        res = await session.execute(
            insert(RolePermission)
            .values(**payload.dict())
            .returning(RolePermission)
        )
        await session.commit()
        return res.scalar_one()
    except IntegrityError:
        await session.rollback()
        # пара вже існує (composite PK) — повернемо 409
        raise HTTPException(status_code=409, detail="Already bound")

# 2. Видалення пари Role - Permission
@router.delete("/bind/{role_name}/{permission_name}", tags=["RolePermissions"])
async def remove_role_permission(
    role_name: str,
    permission_name: str,
    session: AsyncSession = Depends(get_session),
):
    # шукаємо саме у таблиці зв’язок
    res = await session.execute(
        select(RolePermission).where(
            RolePermission.role_name == role_name,
            RolePermission.permission_name == permission_name,
        )
    )
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=f"Bind not found for role='{role_name}', permission='{permission_name}'",
        )

    await session.delete(obj)
    await session.commit()
    return {"ok": True}
