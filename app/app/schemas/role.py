from typing import Optional

from pydantic import BaseModel


# Shared properties
class RoleBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    title: str


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    title: Optional[str] = None


class RoleInDBBase(RoleBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Role(RoleInDBBase):
    pass


# Additional properties stored in DB
class RoleInDB(RoleInDBBase):
    pass
