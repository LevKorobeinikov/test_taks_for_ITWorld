import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.orm import relationship

from app.constants import MAX_LENGHT_EMAIL
from app.models.base import BaseModel


class RoleEnum(str, enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'


class User(BaseModel):
    email = Column(
        String(MAX_LENGHT_EMAIL),
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.now)
    posts = relationship('Post', back_populates='author', lazy='selectin')
    refresh_token = relationship(
        'RefreshToken',
        back_populates='user',
        lazy='selectin',
    )

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr}, '
