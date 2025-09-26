from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.constants import MAX_LENGHT_NAME, MAX_LENGHT_SLUG
from app.models.base import BaseModel


class Category(BaseModel):
    name = Column(
        String(MAX_LENGHT_NAME),
        nullable=False,
        unique=True,
    )
    slug = Column(
        String(MAX_LENGHT_SLUG),
        nullable=False,
        unique=True,
        index=True,
    )
    description = Column(Text, nullable=True)
    posts = relationship(
        'Post',
        back_populates='category',
        lazy='selectin',
    )

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr}, {self.name=}, {self.description=!r}'
