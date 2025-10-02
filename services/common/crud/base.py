from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Type, TypeVar, Generic, List
import logging

log = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        res = await db.execute(select(self.model))
        return res.scalars().all()

    async def get_one(self, db: AsyncSession, pk):
        res = await db.execute(select(self.model).where(self.model.id == pk))
        return res.scalar_one_or_none()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj = self.model(**obj_in.dict())
        db.add(obj)
        try:
            await db.commit()
            await db.refresh(obj)
            return obj
        except IntegrityError as e:
            await db.rollback()
            log.error(f"❌ IntegrityError while creating {self.model.__tablename__}: {e.orig}")
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e.orig)}")

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        try:
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            log.error(f"❌ IntegrityError while updating {self.model.__tablename__}: {e.orig}")
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e.orig)}")

    async def delete(self, db: AsyncSession, db_obj: ModelType):
        await db.delete(db_obj)
        await db.commit()
        return {"status": "deleted"}
