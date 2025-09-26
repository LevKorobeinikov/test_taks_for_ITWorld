from pydantic import BaseModel

from app.constants import TOKEN_TYPE_BEARER


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = TOKEN_TYPE_BEARER
