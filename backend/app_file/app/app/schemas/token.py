from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    mention: List[str]
    role: str
    token_type: str


class TokenPayload(BaseModel):
    uuid: Optional[UUID] = None
    email: Optional[EmailStr]
