from typing import Optional, Any, List
from uuid import UUID

from pydantic import BaseModel

from app.schemas import CollegeYear, NewStudent


# Shared properties
class SubscriptionBase(BaseModel):
    num_carte: Optional[str] = None
    id_year: Optional[UUID]


# Properties to receive via API on creation
class SubscriptionCreate(SubscriptionBase):
    num_carte: str
    id_year: UUID


# Properties to receive via API on update
class SubscriptionUpdate(SubscriptionBase):
    id_year: Optional[UUID]


class SubscriptionInDBBase(SubscriptionBase):
    uuid: Optional[UUID]
    id_year: UUID
    num_carte: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Subscription(SubscriptionInDBBase):
    year: CollegeYear
    student: NewStudent


# Additional properties stored in DB
class SubscriptionInDB(SubscriptionInDBBase):
    pass


class ResponseSubscription(BaseModel):
    count: int
    data: Optional[List[Subscription]]
