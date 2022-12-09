from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils import decode_text
from app import crud, models, schemas
from fastapi.encoders import jsonable_encoder
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_ue(
        *,
        db: Session = Depends(deps.get_db),
        limit: int = 100,
        uuid_journey: str = "",
        semester: str = "",
        offset: int = 0,
        order: str = "asc",
        order_by: str = "title",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve unité d'enseingement.
    """
    ues = crud.teaching_unit.get_multi(db=db, limit=limit, skip=offset, order_by=order_by, order=order,
                                       uuid_journey=uuid_journey, semester = semester)
    list_ue = []
    count = len(crud.teaching_unit.get_count(db=db, uuid_journey=uuid_journey, semester = semester))
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
        if journey:
            ue.journey = journey
            ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    response = schemas.ResponseData(**{'count':count, 'data':list_ue})
    return response


@router.post("/", response_model=List[schemas.MatierUE])
def create_ue(
        *,
        db: Session = Depends(deps.get_db),
        ue_in: schemas.MatierUECreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create unité d'enseingement.
    """
    journey = crud.journey.get_by_uuid(db=db, uuid=ue_in.uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f"Journey not found.", )

    ue_in.value = decode_text(ue_in.title).lower()
    ue_in.key_unique = decode_text(f"{ue_in.value}_{ue_in.semester}_{journey.abbreviation}").lower()
    teaching_unit = crud.teaching_unit.get_by_key_unique(db=db ,key_unique=ue_in.key_unique)
    if teaching_unit:
        raise HTTPException(status_code=404, detail="U.E already exists")
    ues = crud.teaching_unit.create(db=db, obj_in=ue_in)
    ues = crud.teaching_unit.get_all(db=db)
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
        if journey:
            ue.journey = journey
            ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue


@router.put("/", response_model=List[schemas.MatierUE])
def update_ue(
        *,
        db: Session = Depends(deps.get_db),
        ue_in: schemas.MatierUEUpdate,
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update unité d'enseingement.
    """

    ue = crud.teaching_unit.get_by_uuid(db=db, uuid=uuid)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")
    ues = crud.teaching_unit.update(db=db, obj_in=ue_in, db_obj=ue)
    ues = crud.teaching_unit.get_all(db=db)
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
        if journey:
            ue.journey = journey
            ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue

@router.get("/by_uuid/", response_model=schemas.MatierUE)
def get_by_uuid(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update unité d'enseingement.
    """
    ue = crud.teaching_unit.get_by_uuid(db=db, uuid=uuid)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")
    ue = schemas.MatierUE(**jsonable_encoder(ue))
    journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
    if journey:
        ue.journey = journey
        ue.abbreviation_journey = journey.abbreviation
    return ue


@router.get("/get_by_class/"
            "", response_model=List[schemas.MatierUE])
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

    ues = crud.teaching_unit.get_by_class(db=db, uuid_journey=uuid_journey, semester=semester)
    if not ues:
        return []
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        ue.journey = journey
        ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue


@router.get("/get_by_class_with_ec/"
            "", response_model=List[schemas.MatierUEEC])
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

    ues = crud.teaching_unit.get_by_class(db=db, uuid_journey=uuid_journey, semester=semester)
    if not ues:
        return []
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUEEC(**jsonable_encoder(on_ue))
        ecs = crud.constituent_element.get_by_value_ue(db=db, value_ue=ue.value,
                                             semester=semester, uuid_journey=uuid_journey
                                             )
        ue.ec = ecs
        list_ue.append(ue)
    return list_ue


@router.delete("/", response_model=List[schemas.MatierUE])
def delete_ue(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete unité d'enseingements.
    """
    ue = crud.teaching_unit.get_by_uuid(db=db, uuid=uuid)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")

    ecs = crud.constituent_element.get_by_value_ue(db=db,
                                         value_ue=ue.value, semester=ue.semester, uuid_journey=ue.uuid_journey)
    for ec in ecs:
        crud.constituent_element.remove(db=db, id=ec.uuid)
    ues = crud.teaching_unit.remove(db=db, id=uuid)
    ues = crud.teaching_unit.get_all(db=db)
    list_ue = []
    for on_ue in ues:
        ue = schemas.MatierUE(**jsonable_encoder(on_ue))
        journey = crud.journey.get_by_uuid(db=db, uuid=ue.uuid_journey)
        if journey:
            ue.journey = journey
            ue.abbreviation_journey = journey.abbreviation
        list_ue.append(ue)
    return list_ue
