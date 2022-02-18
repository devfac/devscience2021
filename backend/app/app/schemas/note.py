from typing import Any, List
from pydantic import BaseModel


class NoteEC(BaseModel):
    name: str
    note: str


class Note(BaseModel):
    num_carte: str
    name: str
    ec: List[NoteEC]
