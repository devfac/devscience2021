from os import SEEK_HOLE
from typing import Any, List
import uuid, json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.utils import decode_schemas, decode_text

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
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    matier_ec = crud.matier_ec.get_all(schema=schema)
    return matier_ec


@router.get("/by_value_ue", response_model=List[schemas.MatierEC])
def read_by_value_ue(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    value_ue:str,
    semestre:str,
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    matier_ec = crud.matier_ec.get_by_value_ue(schema=schema, 
        value_ue=value_ue, semestre=semestre, uuid_parcours=uuid_parcours)
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
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
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
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
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
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    ec_in.uuid = uuid.uuid4()
    parcours = crud.parcours.get_by_uuid(db=db, uuid=ec_in.uuid_parcours)
    value = decode_text(ec_in.title).lower()
    key_unique = decode_text(f"{value}_{ec_in.semestre}_{parcours.abreviation}").lower()
    matier_ec = crud.matier_ec.get_by_schema(schema=schema, obj_in=ec_in, value=value)
    if matier_ec:
        raise HTTPException(status_code=404, detail="E.C already exists")
    ec = crud.matier_ec.create_ec(schema=schema, obj_in=ec_in,value=value,key_unique=key_unique)
    return ec

@router.put("/update_ec/", response_model=List[schemas.MatierEC])
def update_ec(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    ec_in: schemas.MatierECUpdate,
    uuid:str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    """
    Update élément constitutif.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    ec = crud.matier_ec.get_by_uuid(schema=schema, uuid=uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")
    ec = crud.matier_ec.update_ec(schema=schema, obj_in=ec_in,uuid=uuid)
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
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    ec = crud.matier_ec.get_by_uuid(schema=schema, uuid=uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")

    ec = crud.matier_ec.delete_ec(schema=schema, uuid=uuid)
    return ec
