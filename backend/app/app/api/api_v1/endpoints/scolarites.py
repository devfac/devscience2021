from fastapi import APIRouter, Depends, File
from sqlalchemy.orm import Session
from app import models
from typing import Any
from app.api import deps
from fastapi.responses import FileResponse
from app.scolarite import create_certificat

router = APIRouter()

@router.delete("/certificat")
def certificat(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    file = create_certificat(num_carte)
    return FileResponse(file)