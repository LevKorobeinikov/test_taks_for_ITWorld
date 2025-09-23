from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.core.db import Base


class Post(Base):
    title = Column(String(300), nullable=False)
    slug = Column(String(350), nullable=False, unique=True, index=True)
    content_html = Column(Text, nullable=False)
    content_text = Column(Text, nullable=True)
    is_published = Column(Boolean, default=False, nullable=False)
    author_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
    )
    category_id = Column(
        Integer,
        ForeignKey('categories.id', ondelete='SET NULL'),
        nullable=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    author = relationship('User', back_populates='posts', lazy='joined')
    category = relationship('Category', back_populates='posts', lazy='joined')
