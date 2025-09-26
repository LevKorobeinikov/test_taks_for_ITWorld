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

from app.constants import MAX_LENGHT_SLUG_POST, MAX_LENGHT_TITLE, SET_NULL
from app.models.base import BaseModel


class Post(BaseModel):
    title = Column(String(MAX_LENGHT_TITLE), nullable=False)
    slug = Column(
        String(MAX_LENGHT_SLUG_POST),
        nullable=False,
        unique=True,
        index=True,
    )
    content_html = Column(Text, nullable=False)
    content_text = Column(Text, nullable=True)
    is_published = Column(Boolean, default=False, nullable=False)
    author_id = Column(
        Integer,
        ForeignKey('user.id', ondelete=SET_NULL),
        nullable=True,
    )
    category_id = Column(
        Integer,
        ForeignKey('category.id', ondelete=SET_NULL),
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

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr}, {self.title=}, '
