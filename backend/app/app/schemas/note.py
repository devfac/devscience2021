from typing import Any, List
from pydantic import BaseModel

class NoteEC(BaseModel):
    name:str
    note:float
class Note(BaseModel):
    num_carte: str
    name:str
    ec:Any

