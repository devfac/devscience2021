from typing import Any, List, Optional
from pydantic import BaseModel


class NoteEC(BaseModel):
    name: str
    note: Optional[float]


class NoteUE(BaseModel):
    name: str
    ec: List[NoteEC]


class Note(BaseModel):
    num_carte: str
    ue: List[NoteUE]
