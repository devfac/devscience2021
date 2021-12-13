from typing import Any, List

import sqlalchemy

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.db.session import engine
from sqlalchemy.sql.ddl import CreateSchema
from app.utils import create_anne
from app.core.config import settings

router = APIRouter()



@router.get("/get_notes", response_model=List[Any])
def get_notes(
    schemas: str,
    semestre:str,
    parcours:str,
    session:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

 all_note = crud.note.read_all_note(schemas, semestre, parcours,session)
 return all_note