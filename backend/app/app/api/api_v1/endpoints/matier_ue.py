from os import SEEK_HOLE
from typing import Any, List
import uuid, json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils import UUIDEncoder, decode_text
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.MatierUE])
def read_ue(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Retrieve unité d'enseingement.
    """
    matier_ue = crud.matier_ue.get_all(schema=schema)
    return matier_ue

@router.post("/", response_model=List[schemas.MatierUE])
def create_ue(
    *,
    db: Session = Depends(deps.get_db),
    ue_in: schemas.MatierUECreate,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Create unité d'enseingement.
    """
    ue_in.uuid = uuid.uuid4()
    value = decode_text(ec_in.title).lower()
    matier_ue = crud.matier_ue.get_by_schema(schema=schema, obj_in=ue_in,value=value)
    if matier_ue:
        raise HTTPException(status_code=404, detail="U.E already exists")
    matier_ue = crud.matier_ue.create_ue(schema=schema, obj_in=ue_in,value=value)
    return matier_ue

@router.put("/update_ue/", response_model=List[schemas.MatierUE])
def update_ue(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    ue_in: schemas.MatierUEUpdate,
    uuid:str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Update unité d'enseingement.
    """
    ue = crud.matier_ue.get_by_uuid(schema=schema, uuid=uuid)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")
    ue = crud.matier_ue.update_ue(schema=schema, obj_in=ue_in,uuid=uuid)
    return ue

@router.delete("/delete_ue/", response_model=List[schemas.MatierUE])
def delete_ue(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Delete unité d'enseingements.
    """
    ue = crud.matier_ue.get_by_uuid(schema=schema, uuid=uuid)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")

    ue = crud.matier_ue.delete_ue(schema=schema, uuid=uuid)
    return ue
