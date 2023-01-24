from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ValidationBase(BaseModel):
    s1: Optional[str]
    s2: Optional[str]
    s3: Optional[str]
    s4: Optional[str]
    s5: Optional[str]
    s6: Optional[str]
    s7: Optional[str]
    s8: Optional[str]
    s9: Optional[str]
    s10: Optional[str]
    num_carte: Optional[str]

# Properties to receive via API on creation
class ValidationCreate(ValidationBase):
    pass

# Properties to receive via API on update
class ValidationUpdate(ValidationBase):
    pass

# Properties to receive via API on update
class ValidationInDBBase(ValidationBase):
    uuid: Optional[UUID]
    num_carte: Optional[str]

    class Config:
        orm_mode = True

# Additional properties to return via API
class Validation(ValidationInDBBase):
    pass

# Additional properties stored in DB
class ValidationInDB(ValidationInDBBase):
    pass
