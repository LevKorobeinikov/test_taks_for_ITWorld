from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    ERR_CATEGORY_NOT_FOUND,
    ERR_CATEGORY_SLUG_EXISTS,
)
from app.core.db import get_async_session
from app.crud.category import category_crud
from app.crud.post import post_crud
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.schemas.post import PostRead
from app.utils.security import admin_user

router = APIRouter()


@router.get(
    '/',
    response_model=List[CategoryRead],
    response_model_exclude_none=True,
)
async def list_categories(
    session: AsyncSession = Depends(get_async_session),
):
    return await category_crud.get_multi(session=session)


@router.get(
    '/{slug}/posts',
    response_model=List[PostRead],
    response_model_exclude_none=True,
)
async def list_posts_by_category(
    slug: str,
    session: AsyncSession = Depends(get_async_session),
):
    category = await category_crud.get_by_slug(slug=slug, session=session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_CATEGORY_NOT_FOUND,
        )
    q_posts = await post_crud.list_published(session=session)
    return [p for p in q_posts if p.category_id == category.id]


@router.post(
    '/',
    response_model=CategoryRead,
    dependencies=[Depends(admin_user)],
)
async def create_category(
    data: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для админа."""
    exists = await category_crud.get_by_slug(slug=data.slug, session=session)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_CATEGORY_SLUG_EXISTS,
        )
    return await category_crud.category_create(
        name=data.name,
        slug=data.slug,
        description=data.description,
        session=session,
    )


@router.put(
    '/{slug}',
    response_model=CategoryRead,
    dependencies=[Depends(admin_user)],
)
async def update_category(
    slug: str,
    data: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для админа."""
    category = await category_crud.update_by_slug(
        slug=slug,
        data=data,
        session=session,
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_CATEGORY_NOT_FOUND,
        )
    return category


@router.delete(
    '/{slug}',
    dependencies=[Depends(admin_user)],
)
async def delete_category(
    slug: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для админа."""
    category = await category_crud.get_by_slug(slug=slug, session=session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_CATEGORY_NOT_FOUND,
        )
    await category_crud.remove(category, session=session)
