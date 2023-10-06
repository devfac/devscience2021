from typing import Optional
from datetime import date
from pydantic import BaseModel


# Shared properties
class ReceiptBase(BaseModel):
    num: Optional[str]
    date: Optional[date]
    price: Optional[float]
    id_year: Optional[int]
    num_carte: Optional[str]


# Properties to receive via API on creation
class ReceiptCreate(ReceiptBase):
    num: str
    date: date
    price: float
    id_year: int
    num_carte: str


# Properties to receive via API on update
class ReceiptUpdate(ReceiptBase):
    pass


class ReceiptInDBBase(ReceiptBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Receipt(ReceiptInDBBase):
    pass


# Additional properties stored in DB
class ReceiptInDB(ReceiptInDBBase):
    pass
