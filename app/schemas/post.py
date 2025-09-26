from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.constants import MAX_LENGHT_TITLE, MIN_LENGHT


class PostCreate(BaseModel):
    title: str = Field(..., max_length=MAX_LENGHT_TITLE)
    slug: str
    content_html: str
    category_id: Optional[int]
    is_published: bool = False

    class Config:
        extra = 'forbid'
        min_anystr_length = MIN_LENGHT
        schema_extra = {
            'example': {
                'title': 'New Post',
                'slug': 'new-post',
                'content_html': '<p>Post content</p>',
                'category_id': 1,
                'is_published': False,
            },
        }


class PostRead(BaseModel):
    id: int
    title: str
    slug: str
    content_html: str
    content_text: Optional[str]
    is_published: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
