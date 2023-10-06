from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.utils import decode_text, decode_
from app import crud, models, schemas
from fastapi.encoders import jsonable_encoder
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseTeachingUnit)
def read_ue(
        *,
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        where: List[Any] = Query([], description="Filter conditions"),
        order: str = "asc",
        order_by: str = "title",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve unité d'enseingement.
    """
    ues = crud.teaching_unit.get_multi(
        db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=where)
    count = crud.teaching_unit.get_count(db=db, where=where)
    response = schemas.ResponseData(**{'count': count, 'data': ues})
    return response


@router.post("/", response_model=schemas.TeachingUnit)
def create_ue(
        *,
        db: Session = Depends(deps.get_db),
        ue_in: schemas.TeachingUnitCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create unité d'enseingement.
    """
    journey = crud.journey.get_by_id(db=db, id=ue_in.id_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f"Journey not found.", )

    ue_in.value = decode_text(ue_in.title).lower()
    ue_in.key_unique = decode_text(f"{ue_in.value}_{ue_in.semester}_{journey.abbreviation}").lower()
    teaching_unit = crud.teaching_unit.get_by_key_unique(db=db, key_unique=ue_in.key_unique)
    if teaching_unit:
        raise HTTPException(status_code=404, detail="U.E already exists")
    ue = crud.teaching_unit.create(db=db, obj_in=ue_in)
    return ue


@router.put("/", response_model=schemas.TeachingUnit)
def update_ue(
        *,
        db: Session = Depends(deps.get_db),
        ue_in: schemas.TeachingUnitUpdate,
        id_ue: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update unité d'enseingement.
    """

    ue = crud.teaching_unit.get(db=db, id=id_ue)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")
    ues = crud.teaching_unit.update(db=db, obj_in=ue_in, db_obj=ue)
    return ues


@router.get("/by_id/", response_model=schemas.TeachingUnit)
def get_by_id(
        *,
        db: Session = Depends(deps.get_db),
        id_ue: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update unité d'enseingement.
    """
    ue = crud.teaching_unit.get(db=db, id=id_ue)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")
    return ue


@router.get("/get_by_class/"
            "", response_model=List[schemas.TeachingUnit])
def get_by_class(
        *,
        db: Session = Depends(deps.get_db),
        semester: str,
        id_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    get unité d'enseingement.
    """
    journey = crud.journey.get(db=db, id=id_journey)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    ues = crud.teaching_unit.get_by_class(db=db, id_journey=id_journey, semester=semester)
    return ues


@router.get("/get_by_class_with_ec/"
            "", response_model=List[schemas.UEEC])
def get_by_class(
        *,
        db: Session = Depends(deps.get_db),
        semester: str,
        id_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    get unité d'enseingement.
    """
    journey = crud.journey.get_by_id(db=db, id=id_journey)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    ues = crud.teaching_unit.get_by_class(db=db, id_journey=id_journey, semester=semester)
    if not ues:
        return []
    list_ue = []
    for on_ue in ues:
        ue = schemas.UEEC(**jsonable_encoder(on_ue))
        ecs = crud.constituent_element.get_by_value_ue(db=db, value_ue=ue.value,
                                                       semester=semester, id_journey=id_journey
                                                       )
        ue.ec = ecs
        list_ue.append(ue)
    return list_ue


@router.delete("/", response_model=Any)
def delete_ue(
        *,
        db: Session = Depends(deps.get_db),
        id_ue: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete unité d'enseingements.
    """
    ue = crud.teaching_unit.get(db=db, id=id_ue)
    if not ue:
        raise HTTPException(status_code=404, detail="U.E not found")

    ecs = crud.constituent_element.get_by_value_ue(db=db,
                                                   value_ue=ue.value, semester=ue.semester, id_journey=ue.id_journey)
    for ec in ecs:
        crud.constituent_element.remove(db=db, id=ec.id)
    ues = crud.teaching_unit.remove(db=db, id=id_ue)
    return ues
