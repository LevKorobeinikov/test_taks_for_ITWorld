import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, String, func
from sqlalchemy.orm import relationship

from app.core.db import Base


class RoleEnum(str, enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'


class User(Base):
    email = Column(String(320), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    posts = relationship('Post', back_populates='author', lazy='selectin')
    refresh_tokens = relationship(
        'RefreshToken',
        back_populates='user',
        lazy='selectin',
    )
