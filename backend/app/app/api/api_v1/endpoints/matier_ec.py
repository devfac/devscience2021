from os import SEEK_HOLE
from typing import Any, List
import uuid, json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.utils import decode_text

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


@router.get("/by_value_ue", response_model=List[schemas.MatierEC])
def read_by_value_ue(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    value:str,
    semestre:str,
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    matier_ec = crud.matier_ec.get_by_value_ue(schema=schema, 
        value=value, semestre=semestre, uuid_parcours=uuid_parcours)
    return matier_ec

@router.get("/by_value", response_model=schemas.MatierEC)
def read_by_value(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    value:str,
    semestre:str,
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    matier_ec = crud.matier_ec.get_by_value_ue(schema=schema, 
        value=value, semestre=semestre, uuid_parcours=uuid_parcours)
    return matier_ec

@router.get("/by_uuid", response_model=schemas.MatierEC)
def read_by_uuid(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    uuid:str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Retrieve élément constitutif by uuid.
    """
    matier_ec = crud.matier_ec.get_by_uuid(schema=schema, uuid=uuid)
    if not matier_ec:
        raise HTTPException(status_code=404, detail="E.C not found")
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
    ec_in.value = decode_text(ec_in.title)
    matier_ec = crud.matier_ec.get_by_schema(schema=schema, obj_in=ec_in)
    if matier_ec:
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
    schema: str,
    uuid:str,
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
