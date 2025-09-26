from fastapi import APIRouter

from app.api.endpoints import (
    auth_router,
    categories_router,
    posts_router,
    user_router,
)
from app.constants import (
    API_PREFIX,
    AUTH_PREFIX,
    CATEGORIES_PREFIX,
    POSTS_PREFIX,
    TAG_AUTH,
    TAG_CATEGORIES,
    TAG_POSTS,
    TAG_USERS,
    USERS_PREFIX,
)

api_router = APIRouter(prefix=API_PREFIX)
api_router.include_router(
    auth_router,
    prefix=AUTH_PREFIX,
    tags=[TAG_AUTH],
)
api_router.include_router(
    user_router,
    prefix=USERS_PREFIX,
    tags=[TAG_USERS],
)
api_router.include_router(
    posts_router,
    prefix=POSTS_PREFIX,
    tags=[TAG_POSTS],
)
api_router.include_router(
    categories_router,
    prefix=CATEGORIES_PREFIX,
    tags=[TAG_CATEGORIES],
)
