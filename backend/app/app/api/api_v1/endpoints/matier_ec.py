from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import decode_text

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_ec(
        *,
        db: Session = Depends(deps.get_db),
        limit: int = 100,
        offset: int = 0,
        order: str = "asc",
        order_by: str = "title",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif.
    """
    ecs = crud.constituent_element.get_multi(db=db, limit=limit, skip=offset, order_by=order_by, order=order)
    list_ec = []
    count = len(crud.constituent_element.get_count(db=db))
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    response = schemas.ResponseData(**{'count':count, 'data':list_ec})
    return response

@router.get("/get_by_class/"
            "", response_model=List[schemas.MatierEC])
def get_by_class(
        *,
        db: Session = Depends(deps.get_db),
        semester: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    get unité d'enseingement.
    """
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    ecs = crud.constituent_element.get_by_class(db=db, uuid_journey=uuid_journey, semester=semester)
    if not ecs:
        raise HTTPException(status_code=404, detail="E.C not found")
    list_ec = []
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        ec.journey = journey
        ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec



@router.get("/value_ue/", response_model=List[schemas.MatierEC])
def read_by_value_ue(
        *,
        db: Session = Depends(deps.get_db),
        value_ue: str,
        semester: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    ecs = crud.constituent_element.get_by_value_ue(db=db,value_ue=value_ue,
                                                   semester=semester, uuid_journey=uuid_journey)
    list_ec = []
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec


@router.get("/by_value/", response_model=schemas.MatierEC)
def read_by_value(
        *,
        db: Session = Depends(deps.get_db),
        value: str,
        semester: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    constituent_element = crud.constituent_element.get_by_value(db=db,
                                               value=value, semester=semester, uuid_journey=uuid_journey)
    return constituent_element


@router.get("/by_uuid", response_model=schemas.MatierEC)
def read_by_uuid(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by uuid.
    """
    ec = crud.constituent_element.get_by_uuid(db=db, uuid=uuid)
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
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create élément constitutif.
    """
    journey = crud.journey.get_by_uuid(db=db, uuid=ec_in.uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f"Journey not found.", )

    ec_in.value= decode_text(ec_in.title).lower()
    ec_in.key_unique = decode_text(f"{ec_in.value}_{ec_in.semester}_{journey.abbreviation}").lower()
    constituent_element = crud.constituent_element.get_by_key_unique(db=db, key_unique=ec_in.key_unique)
    if constituent_element:
        raise HTTPException(status_code=404, detail="E.C already exists")
    ecs = crud.constituent_element.create(db=db, obj_in=ec_in)
    ecs = crud.constituent_element.get_all(db=db)
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
        ec_in: schemas.MatierECUpdate,
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update élément constitutif.
    """
    ec = crud.constituent_element.get_by_uuid(db=db, uuid=uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")
    ecs = crud.constituent_element.update(db=db, obj_in=ec_in, db_obj=ec)
    ecs = crud.constituent_element.get_all(db=db)
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
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete élément constitutifs.
    """
    ec = crud.constituent_element.get_by_uuid(db=db, uuid=uuid)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")

    ecs = crud.constituent_element.remove(db=db, id=uuid)
    ecs = crud.constituent_element.get_all(db=db)
    list_ec = []
    for on_ec in ecs:
        ec = schemas.MatierEC(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_uuid(db=db, uuid=ec.uuid_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec
