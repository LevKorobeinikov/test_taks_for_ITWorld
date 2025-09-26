from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.constants import MIN_LENGHT


class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

    class Config:
        extra = 'forbid'
        min_anystr_length = MIN_LENGHT
        schema_extra = {
            'example': {
                'name': 'Mouse for cats',
                'slug': 'mouse-for-cats',
                'description': 'Cats need it',
            },
        }


class CategoryUpdate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

    class Config:
        extra = 'forbid'
        min_anystr_length = MIN_LENGHT


class CategoryRead(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)
