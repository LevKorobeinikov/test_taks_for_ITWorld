from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ERR_INVALID_TOKEN, ERR_USER_NOT_FOUND
from app.core.db import get_async_session
from app.crud.user import user_crud
from app.models.user import RoleEnum
from app.schemas.user import UserRead
from app.utils.security import admin_user, decode_token

bearer = HTTPBearer()
router = APIRouter()


async def current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        payload = decode_token(creds.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERR_INVALID_TOKEN,
        )
    user_id = int(payload.get('sub'))
    user = await user_crud.get(user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERR_USER_NOT_FOUND,
        )
    return user


@router.get('/me', response_model=UserRead)
async def me(user=Depends(current_user)):
    return user


@router.patch(
    '/users/role',
    dependencies=[Depends(admin_user)],
)
async def change_user_role_by_email(
    email: str,
    new_role: RoleEnum,
    session: AsyncSession = Depends(get_async_session),
):
    user = await user_crud.change_role(email, new_role, session)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return {'email': user.email, 'role': user.role}
