from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryUpdate


class CRUDCategory(CRUDBase[Category, object, object]):
    async def get_by_slug(
        self,
        slug: str,
        session: AsyncSession,
    ) -> Optional[Category]:
        query = select(self.model).where(self.model.slug == slug)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def category_create(
        self,
        name: str,
        slug: str,
        description: str | None,
        session: AsyncSession,
        commit: bool = True,
    ) -> Category:
        catogory = Category(name=name, slug=slug, description=description)
        session.add(catogory)
        if commit:
            await session.commit()
            await session.refresh(catogory)
        else:
            await session.flush()
        return catogory

    async def update_by_slug(
        self,
        slug: str,
        data: CategoryUpdate,
        session: AsyncSession,
        commit: bool = True,
    ) -> Optional[Category]:
        category = await self.get_by_slug(slug=slug, session=session)
        if not category:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        session.add(category)
        if commit:
            await session.commit()
            await session.refresh(category)
        else:
            await session.flush()
        return category


category_crud = CRUDCategory(Category)
