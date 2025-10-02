from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.deps.db import get_session
from common.models.config import Command
from common.schemas.config import CommandCreate, CommandUpdate, CommandRead
from common.crud.base import CRUDBase

router = APIRouter(prefix="/commands", tags=["commands"])

# створюємо CRUD екземпляр для Command
crud = CRUDBase[Command, CommandCreate, CommandUpdate](Command)


@router.get("/", response_model=list[CommandRead])
async def list_commands(db: AsyncSession = Depends(get_session)):
    return await crud.get_all(db)


@router.get("/{command_id}", response_model=CommandRead)
async def get_command(command_id: int, db: AsyncSession = Depends(get_session)):
    obj = await crud.get_one(db, command_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Command not found")
    return obj


@router.post("/", response_model=CommandRead)
async def create_command(cmd: CommandCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create(db, cmd)


@router.put("/{command_id}", response_model=CommandRead)
async def update_command(command_id: int, cmd: CommandUpdate, db: AsyncSession = Depends(get_session)):
    obj = await crud.get_one(db, command_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Command not found")
    return await crud.update(db, obj, cmd)


@router.delete("/{command_id}")
async def delete_command(command_id: int, db: AsyncSession = Depends(get_session)):
    obj = await crud.get_one(db, command_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Command not found")
    return await crud.delete(db, obj)
