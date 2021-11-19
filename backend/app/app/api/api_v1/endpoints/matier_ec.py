from os import SEEK_HOLE
from typing import Any, List
import uuid, json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.MatierEC])
def read_ec(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Retrieve élément constitutif.
    """
    matier_ec = crud.matier_ec.get_all(schema=schema)
    return matier_ec

@router.post("/", response_model=List[schemas.MatierEC])
def create_ec(
    *,
    db: Session = Depends(deps.get_db),
    ec_in: schemas.MatierECCreate,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Create élément constitutif.
    """
    ec_in.uuid = uuid.uuid4()
    ec = crud.matier_ec.get_by_value(schema=schema, 
        value=ec_in.value, semestre=ec_in.semestre,uuid_parcours=ec_in.uuid_parcours)
    if ec:
        raise HTTPException(status_code=404, detail="E.C already exists")
    ec = crud.matier_ec.create_ec(schema=schema, obj_in=ec_in)
    return ec

@router.put("/update_ec/", response_model=List[schemas.MatierEC])
def update_ec(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    ec_in: schemas.MatierECUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Update élément constitutif.
    """
    ec = crud.matier_ec.get_by_uuid(schema=schema, uuid=ec_in.uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")
    ec = crud.matier_ec.update_ec(schema=schema, obj_in=ec_in)
    return ec

@router.delete("/delete_ec/", response_model=List[schemas.MatierEC])
def delete_ec(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Delete élément constitutifs.
    """
    ec = crud.matier_ec.get_by_uuid(schema=schema, uuid=uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")

    ec = crud.matier_ec.delete_ec(schema=schema, uuid=uuid)
    return ec
