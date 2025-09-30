from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from common.models.config import Command
from common.schemas.config import CommandSchema
from common.deps.config import get_db

router = APIRouter(prefix="/commands", tags=["commands"])


@router.get("/", response_model=list[CommandSchema])
async def list_commands(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Command))
    return res.scalars().all()


@router.get("/{command_id}", response_model=CommandSchema)
async def get_command(command_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.get(Command, command_id)
    if not res:
        raise HTTPException(404, "Command not found")
    return res


@router.post("/", response_model=CommandSchema)
async def create_command(cmd: CommandSchema, db: AsyncSession = Depends(get_db)):
    obj = Command(**cmd.dict(exclude={"id"}))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{command_id}", response_model=CommandSchema)
async def update_command(command_id: int, cmd: CommandSchema, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Command, command_id)
    if not obj:
        raise HTTPException(404, "Command not found")
    for key, value in cmd.dict(exclude={"id"}).items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{command_id}")
async def delete_command(command_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Command, command_id)
    if not obj:
        raise HTTPException(404, "Command not found")
    await db.delete(obj)
    await db.commit()
    return {"status": "deleted"}
