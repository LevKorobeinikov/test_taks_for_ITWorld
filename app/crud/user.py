from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import RoleEnum, User


class CRUDUser(CRUDBase[User, object, object]):
    async def get_by_email(
        self,
        email: str,
        session: AsyncSession,
    ):
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def change_role(
        self,
        email: str,
        new_role: RoleEnum,
        session: AsyncSession,
    ):
        user = await self.get_by_email(email, session)
        if not user:
            return None
        user.role = new_role
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


user_crud = CRUDUser(User)
