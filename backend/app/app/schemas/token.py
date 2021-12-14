from typing import List, Optional
from uuid import UUID
from app import schemas

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    uuid: Optional[UUID] = None
    mention: List[schemas.Mention]
    role: str
