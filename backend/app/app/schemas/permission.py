from typing import Optional, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class PermissionBase(BaseModel):
    email_sender: Optional[str]
    email: Optional[str]
    type: Optional[str]
    valid_time: Optional[float]
    accepted: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()


# Properties to receive via API on creation
class PermissionCreate(BaseModel):
    email: str
    type: str
    valid_time: float
    accepted: bool


# Properties to receive via API on update
class PermissionUpdate(PermissionBase):
    pass


class PermissionInDBBase(PermissionBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Permission(PermissionInDBBase):
    pass


# Additional properties stored in DB
class PermissionInDB(PermissionInDBBase):
    pass
