from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field

from app.constants import MIN_LENGHT_PASSWORD, ROLE_ADMIN, ROLE_USER


class Role(str, Enum):
    USER = ROLE_USER
    ADMIN = ROLE_ADMIN


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=MIN_LENGHT_PASSWORD)

    class Config:
        extra = 'forbid'
        min_anystr_length = MIN_LENGHT_PASSWORD
        schema_extra = {
            'example': {
                'email': 'admin@example.com',
                'password': 'supersecurepassword',
            },
        }


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: Role
    created_at: datetime
    model_config = {'from_attributes': True}
