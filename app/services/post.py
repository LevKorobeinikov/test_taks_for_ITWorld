from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import FIELD_CONTENT_HTML
from app.crud.category import category_crud
from app.crud.post import post_crud
from app.models.post import Post
from app.utils.content import prepare_post_content


class PostService:
    def __init__(
        self,
        post_crud_instance=post_crud,
        category_crud_instance=category_crud,
    ):
        self.post_crud = post_crud_instance
        self.category_crud = category_crud_instance

    async def create_post(
        self,
        title: str,
        slug: str,
        content_html: str,
        author_id: int | None,
        category_id: int | None,
        is_published: bool,
        session: AsyncSession,
    ):
        prepared = prepare_post_content({FIELD_CONTENT_HTML: content_html})
        return await self.post_crud.create_post(
            title=title,
            slug=slug,
            content_html=prepared.get(FIELD_CONTENT_HTML),
            author_id=author_id,
            category_id=category_id,
            is_published=is_published,
            session=session,
        )

    async def update_post(
        self,
        post: Post,
        session: AsyncSession,
        **fields,
    ):
        prepared_fields = prepare_post_content(fields)
        for field, value in prepared_fields.items():
            setattr(post, field, value)
        return await self.post_crud.save(post, session=session)
