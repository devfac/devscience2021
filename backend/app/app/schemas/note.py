from typing import Any, List, Optional
from pydantic import BaseModel


class NoteEC(BaseModel):
    name: str
    note: Optional[str]


class NoteUE(BaseModel):
    num_carte:  Optional[str]
    name:  Optional[str]
    ec: Optional[List[NoteEC]]


class Note(BaseModel):
    num_carte:  Optional[str]
    ue: Optional[List[NoteUE]]
