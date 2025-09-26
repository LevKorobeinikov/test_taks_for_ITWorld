from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import LIMIT, OFFSET, USER_ID

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType')
UpdateSchemaType = TypeVar('UpdateSchemaType')


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
        limit: int = LIMIT,
        offset: int = OFFSET,
    ) -> list[ModelType]:
        query = select(self.model).limit(limit).offset(offset)
        result = await session.execute(query)
        return result.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: object | None = None,
        commit: bool = True,
    ) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict()
        if user is not None and hasattr(self.model, USER_ID):
            obj_in_data[USER_ID] = getattr(user, 'id')
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        else:
            await session.flush()
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        else:
            await session.flush()
        return db_obj

    async def remove(self, db_obj, session: AsyncSession) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
