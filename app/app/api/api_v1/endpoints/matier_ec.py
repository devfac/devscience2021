from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import decode_text, decode_

router = APIRouter()


@router.get("/", response_model=schemas.ResponseConstituentElement)
def read_ec(
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
    Retrieve élément constitutif.
    """
    ecs = crud.constituent_element.get_multi(
        db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=where)
    count = crud.constituent_element.get_count(db=db, where=where)
    response = schemas.ResponseConstituentElement(**{'count': count, 'data': ecs})
    return response


@router.get("/get_by_class/"
            "", response_model=List[schemas.ConstituentElement])
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

    ecs = crud.constituent_element.get_by_class(db=db, id_journey=id_journey, semester=semester)
    return ecs


@router.get("/value_ue/", response_model=List[schemas.ConstituentElement])
def read_by_value_ue(
        *,
        db: Session = Depends(deps.get_db),
        value_ue: str,
        semester: str,
        id_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    ecs = crud.constituent_element.get_by_value_ue(db=db, value_ue=value_ue,
                                                   semester=semester, id_journey=id_journey)
    list_ec = []
    for on_ec in ecs:
        ec = schemas.ConstituentElement(**jsonable_encoder(on_ec))
        journey = crud.journey.get_by_id(db=db, uuid=ec.id_journey)
        if journey:
            ec.journey = journey
            ec.abbreviation_journey = journey.abbreviation
        list_ec.append(ec)
    return list_ec


@router.get("/by_value/", response_model=schemas.ConstituentElement)
def read_by_value(
        *,
        db: Session = Depends(deps.get_db),
        value: str,
        semester: str,
        id_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by value_ue.
    """
    constituent_element = crud.constituent_element.get_by_value(db=db,
                                                                value=value, semester=semester,
                                                                id_journey=id_journey)
    return constituent_element


@router.get("/by_id", response_model=schemas.ConstituentElement)
def read_by_id(
        *,
        db: Session = Depends(deps.get_db),
        id_ec: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve élément constitutif by uuid.
    """
    ec = crud.constituent_element.get(db=db, id=id_ec)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")
    return ec


@router.post("/", response_model=schemas.ConstituentElement)
def create_ec(
        *,
        db: Session = Depends(deps.get_db),
        ec_in: schemas.ConstituentElementCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create élément constitutif.
    """
    journey = crud.journey.get(db=db, id=ec_in.id_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f"Journey not found.", )

    ec_in.value = decode_text(ec_in.title).lower()
    ec_in.key_unique = decode_text(f"{ec_in.value}_{ec_in.semester}_{journey.abbreviation}").lower()
    constituent_element = crud.constituent_element.get_by_key_unique(db=db, key_unique=ec_in.key_unique)
    if constituent_element:
        raise HTTPException(status_code=404, detail="E.C already exists")
    ec = crud.constituent_element.create(db=db, obj_in=ec_in)
    return ec


@router.put("/", response_model=schemas.ConstituentElement)
def update_ec(
        *,
        db: Session = Depends(deps.get_db),
        ec_in: schemas.ConstituentElementUpdate,
        id_ec: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update élément constitutif.
    """
    ec = crud.constituent_element.get(db=db, id=id_ec)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")
    ecs = crud.constituent_element.update(db=db, obj_in=ec_in, db_obj=ec)
    return ecs


@router.delete("/", response_model=Any)
def delete_ec(
        *,
        db: Session = Depends(deps.get_db),
        id_ec: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete élément constitutifs.
    """
    ec = crud.constituent_element.get(db=db, id=id_ec)
    if not ec:
        raise HTTPException(status_code=404, detail="E.C not found")
    ecs = crud.constituent_element.remove(db=db, id=id_ec)
    return ecs