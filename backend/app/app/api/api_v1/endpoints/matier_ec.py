from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import decode_text, create_anne

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
    anne_univ = crud.college_year.get_by_title(db, schema)
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ecs = crud.matier_ec.get_all(schema=create_anne(schema))
    list_ec = []
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec


@router.get("/{value_ue}", response_model=List[schemas.MatierEC])
def read_by_value_ue(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        value_ue: str,
        semester: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    anne_univ = crud.college_year.get_by_title(db, schema)
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ecs = crud.matier_ec.get_by_value_ue(schema=create_anne(schema),
                                               value_ue=value_ue, semester=semester, uuid_journey=uuid_journey)
    list_ec = []
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec


@router.get("/{value}", response_model=schemas.MatierEC)
def read_by_value(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        value: str,
        semester: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    anne_univ = crud.college_year.get_by_title(db, schema=schema)
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    matier_ec = crud.matier_ec.get_by_value(schema=create_anne(schema),
                                               value=value, semester=semester, uuid_journey=uuid_journey)
    return matier_ec


@router.get("/{uuid}/", response_model=schemas.MatierEC)
def read_by_uuid(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by uuid.
    """
    anne_univ = crud.college_year.get_by_title(db, schema)
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ec = crud.matier_ec.get_by_uuid(schema=create_anne(schema), uuid=uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")
    ec = schemas.MatierEC(**jsonable_encoder(ec))
    journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
    if journey:
        ec.journey = journey
        ec.abbreviation_journey = journey.abbreviation
    print(ec)
    return ec


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
    anne_univ = crud.college_year.get_by_title(db, schema)
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    journey = crud.journey.get_by_uuid(db=db, uuid=ec_in.uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f"Journey not found.", )

    value = decode_text(ec_in.title).lower()
    key_unique = decode_text(f"{value}_{ec_in.semester}_{journey.abbreviation}").lower()
    matier_ec = crud.matier_ec.get_by_schema(schema=create_anne(schema), obj_in=ec_in, value=value)
    if matier_ec:
        raise HTTPException(status_code=404, detail="E.C already exists")
    ecs = crud.matier_ec.create_ec(schema=create_anne(schema), obj_in=ec_in, value=value, key_unique=key_unique)
    list_ec = []
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec


@router.put("/", response_model=List[schemas.MatierEC])
def update_ec(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        ec_in: schemas.MatierECUpdate,
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update élément constitutif.
    """
    college_year = crud.college_year.get_by_title(db, title=schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ec = crud.matier_ec.get_by_uuid(schema=create_anne(schema), uuid=uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")
    ecs = crud.matier_ec.update_ec(schema=create_anne(schema), obj_in=ec_in, uuid=uuid)
    list_ec = []
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec


@router.delete("/", response_model=List[schemas.MatierEC])
def delete_ec(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete élément constitutifs.
    """
    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.", )
    ec = crud.matier_ec.get_by_uuid(schema=create_anne(schema), uuid=uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")

    ecs = crud.matier_ec.delete_ec(schema=create_anne(schema), uuid=uuid)
    list_ec = []
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec
