from typing import Any
from pydantic import BaseModel


class Note(BaseModel):
    num_carte: str
    note:Any
