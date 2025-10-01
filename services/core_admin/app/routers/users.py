from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.hash import bcrypt
from typing import List
from uuid import UUID
import uuid
import hashlib

from common.deps.db import get_session
from common.models.users import User
from common.schemas.users import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

# ----------------------------------------------------------------
# helpers
# ----------------------------------------------------------------
def hash_password(password: str) -> str:
    """Безпечне хешування: SHA-256 → bcrypt"""
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.hash(digest)
def verify_password(password: str, hashed: str) -> bool:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.verify(digest, hashed)

# ----------------------------------------------------------------
# List users
# ----------------------------------------------------------------
@router.get("/", response_model=List[UserOut])
async def list_users(
    limit: int = Query(200, le=1000),
    session: AsyncSession = Depends(get_session),
):
    res = await session.execute(select(User).limit(limit))
    return res.scalars().all()

# ----------------------------------------------------------------
# Create user
# ----------------------------------------------------------------
@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    raw_password = user.password.get_secret_value()
    hashed_pw = hash_password(raw_password)

    new_user = User(
        user_id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        role=user.role,
        password_hash=hashed_pw,
        is_active=user.is_active,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

# ----------------------------------------------------------------
# Update user
# ----------------------------------------------------------------
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, data: UserUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.dict(exclude_unset=True)

    if "new_password" in update_data and update_data["new_password"]:
        raw_password = update_data.pop("new_password").get_secret_value()
        obj.password_hash = hash_password(raw_password)

    for k, v in update_data.items():
        setattr(obj, k, v)

    await session.commit()
    await session.refresh(obj)
    return obj

# ----------------------------------------------------------------
# Delete user
# ----------------------------------------------------------------
@router.delete("/{user_id}")
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(obj)
    await session.commit()
    return {"ok": True}
