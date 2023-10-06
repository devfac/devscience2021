from typing import Optional, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class InvitationBase(BaseModel):
    email: Optional[str]
    email_from: Optional[str]
    message: Optional[str]
    is_ready: Optional[bool] = False


# Properties to receive via API on creation
class InvitationCreate(InvitationBase):
    email: str
    email_from: str
    message: str


# Properties to receive via API on update
class InvitationUpdate(BaseModel):
    is_ready: bool = True


class InvitationInDBBase(InvitationBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Invitation(InvitationInDBBase):
    pass


# Additional properties stored in DB
class InvitationInDB(InvitationInDBBase):
    pass
