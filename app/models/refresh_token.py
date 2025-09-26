from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.constants import CASCADE, MAX_LENGHT_JTI
from app.models.base import BaseModel


class RefreshToken(BaseModel):
    jti = Column(
        String(MAX_LENGHT_JTI),
        nullable=False,
        unique=True,
        index=True,
    )
    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete=CASCADE),
        nullable=False,
    )
    issued_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    user = relationship('User', back_populates='refresh_token', lazy='joined')

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr}, '
