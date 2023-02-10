from datetime import date
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


# shared properties
class PublicationBase(BaseModel):
    title: Optional[str] = None
    auteur: Optional[str] = None
    url_file: Optional[List[str]] = None
    visibility: Optional[List[str]] = None
    type: Optional[str] = "text"
    description: Optional[str] = None
    expiration_date: Optional[date]


# this will be used to validate data while creating a Publication
class PublicationCreate(PublicationBase):
    title: str
    auteur: str
    url_file: Optional[List[str]]
    visibility: Optional[List[str]]
    description: str
    type: str
    expiration_date: datetime


class PublicationUpdate(PublicationBase):
    pass


# this will be used to format the response to not have uuid,owner_id etc
class ShowPublication(PublicationBase):
    uuid: Optional[UUID]
    title: str
    auteur: str
    url_file: Optional[List[str]]
    visibility: Optional[List[str]]
    type: str
    created_at: datetime

    class Config:  # to convert non dict obj to json
        orm_mode = True
