from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.deps.db import get_session
from app.models.auth import User
from app.schemas.auth import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserOut])
async def list_users(limit: int = Query(200, le=1000), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(User).limit(limit))
    return res.scalars().all()

@router.post("/", response_model=UserOut)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    obj = User(**data.dict())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    await session.commit()
    await session.refresh(obj)
    return obj

@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    obj = await session.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(obj)
    await session.commit()
    return {"ok": True}
