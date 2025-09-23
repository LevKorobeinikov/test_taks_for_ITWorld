from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Category(Base):
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(150), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    posts = relationship('Post', back_populates='category', lazy='selectin')
