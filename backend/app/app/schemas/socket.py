from fastapi import WebSocket
from pydantic import BaseModel



class SocketModel(BaseModel):
    id: str
    wb: WebSocket
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
