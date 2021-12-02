from typing import List, Optional, Any
from uuid import UUID, uuid4

from sqlalchemy.sql.sqltypes import String

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool]
    is_superuser: bool = False
    first_name: str
    last_name:Optional[str]
    uuid_mention: Optional[List[str]]
    uuid_role: Optional[str]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    first_name: str
    last_name:Optional[str]


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
