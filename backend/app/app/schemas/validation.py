from typing import Optional
from pydantic import BaseModel


class ValidationUpdate(BaseModel):
    num_carte: Optional[str]
    validation: Optional[bool] = False