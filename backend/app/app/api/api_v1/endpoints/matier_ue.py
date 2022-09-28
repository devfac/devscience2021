from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils import decode_text, create_anne
from app import crud, models, schemas
from fastapi.encoders import jsonable_encoder
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
    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ues = crud.matier_ue.get_all(schema=create_anne(schema))
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
        if journey:
            ue.journey = journey
            ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue


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
    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )

    journey = crud.journey.get_by_uuid(db=db, uuid=ue_in.uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f"Journey not found.", )

    value = decode_text(ue_in.title).lower()
    key_unique = decode_text(f"{value}_{ue_in.semester}_{journey.abbreviation}").lower()
    matier_ue = crud.matier_ue.get_by_schema(schema=create_anne(schema), obj_in=ue_in, value=value)
    if matier_ue:
        raise HTTPException(status_code=404, detail="U.E already exists")
    ues = crud.matier_ue.create_ue(schema=create_anne(schema), obj_in=ue_in, value=value, key_unique=key_unique)
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
        if journey:
            ue.journey = journey
            ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue


@router.put("/{uuid}", response_model=List[schemas.MatierUE])
def update_ue(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        ue_in: schemas.MatierUEUpdate,
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update unité d'enseingement.
    """
    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ue = crud.matier_ue.get_by_uuid(schema=create_anne(schema), uuid=uuid)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")
    ues = crud.matier_ue.update_ue(schema=create_anne(schema), obj_in=ue_in, uuid=uuid)
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
        if journey:
            ue.journey = journey
            ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue


@router.get("/{uuid}", response_model=schemas.MatierUE)
def get_by_uuid(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update unité d'enseingement.
    """
    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ue = crud.matier_ue.get_by_uuid(schema=create_anne(schema), uuid=uuid)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")
    ue = schemas.MatierUE(**jsonable_encoder(ue))
    journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
    if journey:
        ue.journey = journey
        ue.abbreviation_journey = journey.abbreviation
    return ue

@router.get("/{semester}/{uuid_journey}/"
            "", response_model=List[schemas.MatierUE])
def get_by_class(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    get unité d'enseingement.
    """
    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    ues = crud.matier_ue.get_by_class(schema=create_anne(schema), uuid_journey=uuid_journey, semester=semester)
    if not ues:
        raise HTTPException(status_code=404, detail="U.E not found")
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        ue.journey = journey
        ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue


@router.delete("/{uuid}", response_model=List[schemas.MatierUE])
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
    college_year = crud.college_year.get_by_title(db=db, title=schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ue = crud.matier_ue.get_by_uuid(schema=create_anne(schema), uuid=uuid)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")

    ecs = crud.matier_ec.get_by_value_ue(schema=create_anne(schema),
                                         value_ue=ue.value, semester=ue.semester, uuid_journey=ue.uuid_journey)
    for ec in ecs:
        crud.matier_ec.delete_ec(schema=create_anne(schema), uuid=ec.uuid)
    ues = crud.matier_ue.delete_ue(schema=create_anne(schema), uuid=uuid)
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
        if journey:
            ue.journey = journey
            ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue
