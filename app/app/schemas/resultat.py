from typing import Any, List, Optional
from pydantic import BaseModel


class Resultat(BaseModel):
    list_valide: Optional[List[Any]]
    list_non_valide: Optional[List[Any]]
