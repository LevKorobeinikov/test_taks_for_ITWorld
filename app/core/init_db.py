from sqlalchemy import select

from app.constants import ROLE_ADMIN
from app.core.config import settings
from app.core.db import AsyncSessionLocal, Base, engine
from app.models.user import User
from app.utils.security import hash_password


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await create_admin_if_not_exists()


async def create_admin_if_not_exists():
    if (
        not settings.FIRST_SUPERUSER_EMAIL or
        not settings.FIRST_SUPERUSER_PASSWORD
    ):
        return

    async with AsyncSessionLocal() as session:
        admin_check = await session.execute(
            select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL),
        )
        admin = admin_check.scalar_one_or_none()
        if not admin:
            hashed_password = hash_password(settings.FIRST_SUPERUSER_PASSWORD)
            admin = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                hashed_password=hashed_password,
                role=ROLE_ADMIN,
            )
            session.add(admin)
            await session.commit()
            await session.refresh(admin)
