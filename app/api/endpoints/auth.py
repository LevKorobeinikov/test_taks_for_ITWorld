from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    CLAIM_JTI,
    ERR_FAILED_TO_CREATE_TOKENS,
    ERR_INVALID_CREDENTIALS,
    ERR_INVALID_TOKEN,
    ERR_MISSING_REFRESH_TOKEN,
    TOKEN_TYPE_BEARER,
)
from app.core.db import get_async_session
from app.schemas.auth import TokenPair
from app.schemas.user import UserCreate
from app.services.auth import AuthService
from app.utils.security import decode_token

router = APIRouter()
auth_service = AuthService()


async def authenticate_user(
    email: str,
    password: str,
    session: AsyncSession,
    fail_status: int,
    fail_detail: str,
):
    auth = await auth_service.authenticate(
        email,
        password,
        session=session,
    )
    if not auth:
        raise HTTPException(
            status_code=fail_status,
            detail=fail_detail,
        )
    return {
        'access_token': auth['access_token'],
        'refresh_token': auth['refresh_token'],
        'token_type': TOKEN_TYPE_BEARER,
    }


@router.post('/register', response_model=TokenPair)
async def register(
    data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        await auth_service.register(data, session=session)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
    return await authenticate_user(
        data.email,
        data.password,
        session,
        fail_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        fail_detail=ERR_FAILED_TO_CREATE_TOKENS,
    )


@router.post('/login', response_model=TokenPair)
async def login(
    data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await authenticate_user(
        data.email,
        data.password,
        session,
        fail_status=status.HTTP_401_UNAUTHORIZED,
        fail_detail=ERR_INVALID_CREDENTIALS,
    )


@router.post('/refresh', response_model=TokenPair)
async def refresh(
    payload: dict,
    session: AsyncSession = Depends(get_async_session),
):
    refresh_token = payload.get('refresh_token')
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_MISSING_REFRESH_TOKEN,
        )
    try:
        new_tokens = await auth_service.refresh(refresh_token, session=session)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )
    return {
        'access_token': new_tokens['access_token'],
        'refresh_token': new_tokens['refresh_token'],
        'token_type': TOKEN_TYPE_BEARER,
    }


@router.post('/logout')
async def logout(
    payload: dict,
    session: AsyncSession = Depends(get_async_session),
):
    refresh_token = payload.get('refresh_token')
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_MISSING_REFRESH_TOKEN,
        )
    try:
        token = decode_token(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_INVALID_TOKEN,
        )
    jti = token.get(CLAIM_JTI)
    await auth_service.revoke_refresh(jti, session=session)
