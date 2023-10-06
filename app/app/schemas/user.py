from typing import List, Optional

from pydantic import BaseModel, EmailStr

from .role import Role
from .user_mention import UserMention


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool]
    is_superuser: bool = False
    first_name: Optional[str]
    last_name: Optional[str]
    id_role: Optional[int]
    id_mention: Optional[List[int]]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    first_name: str
    last_name: Optional[str]


# Properties to receive via API on update
class UserUpdate(UserBase):
    id_mention: Optional[List[int]]
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    role: Optional[Role]
    list_mention: Optional[List[UserMention]]


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class UserLogin(UserBase):
    role: Optional[str]
    access_token: Optional[str]


class ResponseUser(BaseModel):
    count: int
    data: Optional[List[User]]