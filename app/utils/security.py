from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    CLAIM_EXP,
    CLAIM_IAT,
    CLAIM_JTI,
    CLAIM_SUB,
    CLAIM_TYPE,
    ERR_INVALID_TOKEN,
    ERR_PERMISSION_DENIED,
    REFRESH_EXPIRES_AT,
    REFRESH_ISSUED_AT,
    ROLE_ADMIN,
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
)
from app.core.config import get_auth_data, settings
from app.core.db import get_async_session
from app.crud.user import user_crud

pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')
bearer = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd.verify(password, hashed)


def _now() -> datetime:
    return datetime.now()


def _encode_token(payload: dict) -> str:
    """Вспомогательная функция для кодирования JWT."""
    auth_config = get_auth_data()
    return jwt.encode(
        payload,
        auth_config['secret_key'],
        algorithm=auth_config['algorithm'],
    )


def create_access_token(user_id: int) -> dict:
    now = _now()
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        CLAIM_SUB: str(user_id),
        CLAIM_TYPE: TOKEN_TYPE_ACCESS,
        CLAIM_IAT: int(now.timestamp()),
        CLAIM_EXP: int(expire.timestamp()),
    }
    token = _encode_token(payload)
    return {'token': token, 'expires_at': expire}


def create_refresh_token(user_id: int) -> dict:
    now = _now()
    expire = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid4())
    payload = {
        CLAIM_SUB: str(user_id),
        CLAIM_TYPE: TOKEN_TYPE_REFRESH,
        CLAIM_JTI: jti,
        CLAIM_IAT: int(now.timestamp()),
        CLAIM_EXP: int(expire.timestamp()),
    }
    token = _encode_token(payload)
    return {
        'token': token,
        CLAIM_JTI: jti,
        REFRESH_ISSUED_AT: now,
        REFRESH_EXPIRES_AT: expire,
    }


def decode_token(token: str) -> dict:
    auth_config = get_auth_data()
    return jwt.decode(
        token,
        auth_config['secret_key'],
        algorithms=[auth_config['algorithm']],
    )


async def admin_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    session: AsyncSession = Depends(get_async_session),
):
    token = creds.credentials
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERR_INVALID_TOKEN,
        )
    user_id = int(payload.get(CLAIM_SUB))
    user = await user_crud.get(user_id, session=session)
    if not user or user.role.name != ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERR_PERMISSION_DENIED,
        )
    return user
