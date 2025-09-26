from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import LIMIT, OFFSET
from app.crud.base import CRUDBase
from app.models.post import Post


class CRUDPost(CRUDBase[Post, object, object]):
    async def get_by_slug(
        self,
        slug: str,
        session: AsyncSession,
    ) -> Optional[Post]:
        query = select(self.model).where(self.model.slug == slug)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def list_published(
        self,
        session: AsyncSession,
        limit: int = LIMIT,
        offset: int = OFFSET,
    ) -> list[Post]:
        query = (
            select(self.model)
            .where(self.model.is_published.is_(True))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def create_post(
        self,
        title: str,
        slug: str,
        content_html: str,
        author_id: int | None,
        category_id: int | None,
        is_published: bool,
        session: AsyncSession,
        commit: bool = True,
    ) -> Post:
        post = Post(
            title=title,
            slug=slug,
            content_html=content_html,
            content_text=(content_html or '')[:400],
            author_id=author_id,
            category_id=category_id,
            is_published=is_published,
        )
        session.add(post)
        if commit:
            await session.commit()
            await session.refresh(post)
        else:
            await session.flush()
        return post

    async def save(
        self,
        post: Post,
        session: AsyncSession,
        commit: bool = True,
    ) -> Post:
        session.add(post)
        if commit:
            await session.commit()
            await session.refresh(post)
        else:
            await session.flush()
        return post


post_crud = CRUDPost(Post)
