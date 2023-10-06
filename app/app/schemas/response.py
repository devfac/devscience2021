from typing import Any, List, Optional
from pydantic import BaseModel


class ResponseData(BaseModel):
    count: Optional[int]
    data: Optional[List[Any]]