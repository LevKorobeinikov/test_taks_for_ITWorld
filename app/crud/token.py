from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class CRUDToken:
    async def create(
        self,
        jti: str,
        user_id: int,
        issued_at: datetime,
        expires_at: datetime,
        session: AsyncSession,
    ):
        token = RefreshToken(
            jti=jti,
            user_id=user_id,
            issued_at=issued_at,
            expires_at=expires_at,
        )
        session.add(token)
        await session.commit()
        await session.refresh(token)
        return token

    async def get_by_jti(
        self,
        jti: str,
        session: AsyncSession,
    ) -> Optional[RefreshToken]:
        query = select(RefreshToken).where(RefreshToken.jti == jti)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def revoke(self, jti: str, session: AsyncSession) -> bool:
        token = await self.get_by_jti(jti, session=session)
        if token:
            token.revoked = True
            await session.commit()
            return True
        return False


token_crud = CRUDToken()
