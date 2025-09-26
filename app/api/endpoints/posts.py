from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ERR_POST_NOT_FOUND
from app.core.db import get_async_session
from app.crud.post import post_crud
from app.schemas.post import PostCreate, PostRead
from app.services.post import PostService
from app.utils.security import admin_user

router = APIRouter()
post_service = PostService()


@router.get(
    '/',
    response_model=list[PostRead],
    response_model_exclude_none=True,
)
async def list_posts(session: AsyncSession = Depends(get_async_session)):
    return await post_crud.list_published(session=session)


@router.get(
    '/{slug}',
    response_model=PostRead,
    response_model_exclude_none=True,
)
async def get_post(
    slug: str,
    session: AsyncSession = Depends(get_async_session),
):
    post = await post_crud.get_by_slug(slug=slug, session=session)
    if not post or not post.is_published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_POST_NOT_FOUND,
        )
    return post


@router.post(
    '/',
    response_model=PostRead,
    response_model_exclude_none=True,
)
async def create_post(
    data: PostCreate,
    user=Depends(admin_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Только для админа."""
    return await post_service.create_post(
        title=data.title,
        slug=data.slug,
        content_html=data.content_html,
        author_id=user.id,
        category_id=data.category_id,
        is_published=data.is_published,
        session=session,
    )


@router.put(
    '/{slug}',
    response_model=PostRead,
    response_model_exclude_none=True,
    dependencies=[Depends(admin_user)],
)
async def update_post(
    slug: str,
    data: PostCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для админа."""
    post = await post_crud.get_by_slug(slug=slug, session=session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_POST_NOT_FOUND,
        )
    return await post_service.update_post(
        post,
        session=session,
        title=data.title,
        content_html=data.content_html,
        slug=data.slug,
        category_id=data.category_id,
        is_published=data.is_published,
    )


@router.delete(
    '/{slug}',
    dependencies=[Depends(admin_user)],
)
async def delete_post(
    slug: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для админа."""
    post = await post_crud.get_by_slug(slug=slug, session=session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_POST_NOT_FOUND,
        )
    await post_crud.remove(post, session=session)
