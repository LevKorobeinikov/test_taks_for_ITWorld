from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from uuid import uuid4

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings


settings = get_settings()


pwd_context = CryptContext(
    schemes=[settings.password_hash_scheme, "argon2"],
    deprecated="auto",
)


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(subject: str | int, expires_minutes: int | None = None) -> str:
    expire_minutes = expires_minutes or settings.access_token_expire_minutes
    expire = _now() + timedelta(minutes=expire_minutes)
    to_encode: Dict[str, Any] = {"sub": str(subject), "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str | int, expires_days: int | None = None) -> tuple[str, str, datetime]:
    expire_days = expires_days or settings.refresh_token_expire_days
    expire = _now() + timedelta(days=expire_days)
    jti = uuid4().hex
    to_encode: Dict[str, Any] = {"sub": str(subject), "jti": jti, "exp": expire}
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return token, jti, expire


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])


