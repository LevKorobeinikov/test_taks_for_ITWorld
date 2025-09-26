from sqlalchemy import Column, Integer

from app.core.db import Base


class BaseModel(Base):
    """Абстрактная базовая модель для моделей."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'{type(self).__name__}({self.id=}, '
