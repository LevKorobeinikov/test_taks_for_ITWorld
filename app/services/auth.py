from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    CLAIM_JTI,
    CLAIM_SUB,
    CLAIM_TYPE,
    ERR_INVALID_TOKEN,
    ERR_INVALID_TOKEN_TYPE,
    ERR_TOKEN_REVOKED_OR_NOT_FOUND,
    ERR_USER_ALREADY_EXISTS,
    REFRESH_EXPIRES_AT,
    REFRESH_ISSUED_AT,
    TOKEN_TYPE_REFRESH,
)
from app.crud.token import token_crud
from app.crud.user import user_crud
from app.schemas.user import UserCreate
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class AuthService:
    def __init__(
        self,
        user_crud_instance=user_crud,
        token_crud_instance=token_crud,
    ):
        self.user_crud = user_crud_instance
        self.token_crud = token_crud_instance

    async def register(
        self,
        data: UserCreate,
        session: AsyncSession,
    ):
        existing = await self.user_crud.get_by_email(
            data.email,
            session=session,
        )
        if existing:
            raise ValueError(ERR_USER_ALREADY_EXISTS)
        db_obj_data = data.model_dump(exclude={"password"})
        db_obj_data["hashed_password"] = hash_password(data.password)
        await self.user_crud.create(db_obj_data, session=session)

    async def authenticate(
        self,
        email: str,
        password: str,
        session: AsyncSession,
    ) -> Optional[dict]:
        user = await self.user_crud.get_by_email(email, session=session)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        access = create_access_token(user.id)
        refresh = create_refresh_token(user.id)
        await self.token_crud.create(
            jti=refresh[CLAIM_JTI],
            user_id=user.id,
            issued_at=refresh[REFRESH_ISSUED_AT],
            expires_at=refresh[REFRESH_EXPIRES_AT],
            session=session,
        )
        return {
            'access_token': access['token'],
            'refresh_token': refresh['token'],
            'user': user,
        }

    async def refresh(
        self,
        refresh_token: str,
        session: AsyncSession,
    ) -> dict:
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise ValueError(ERR_INVALID_TOKEN)
        if payload.get(CLAIM_TYPE) != TOKEN_TYPE_REFRESH:
            raise ValueError(ERR_INVALID_TOKEN_TYPE)
        jti = payload.get(CLAIM_JTI)
        user_id = int(payload.get(CLAIM_SUB))
        token_record = await self.token_crud.get_by_jti(jti, session=session)
        if not token_record or token_record.revoked:
            raise ValueError(ERR_TOKEN_REVOKED_OR_NOT_FOUND)
        access = create_access_token(user_id)
        new_refresh = create_refresh_token(user_id)
        await self.token_crud.revoke(jti, session=session)
        await self.token_crud.create(
            jti=new_refresh[CLAIM_JTI],
            user_id=user_id,
            issued_at=new_refresh[REFRESH_ISSUED_AT],
            expires_at=new_refresh[REFRESH_EXPIRES_AT],
            session=session,
        )
        return {
            'access_token': access['token'],
            'refresh_token': new_refresh['token'],
        }

    async def revoke_refresh(
        self,
        jti: str,
        session: AsyncSession,
    ) -> bool:
        return await self.token_crud.revoke(jti, session=session)
