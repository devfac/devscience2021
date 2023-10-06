from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseJourney)
def read_journey(
        db: Session = Depends(deps.get_db),
        *,
        limit: int = 100,
        offset: int = 0,
        order: str = "asc",
        order_by: str = "title",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve paarcours.
    """
    journeys = crud.journey.get_multi(db=db, limit=limit, skip=offset, order_by=order_by, order=order)
    count = crud.journey.get_count(db=db)
    all_journeys = []
    for journey in journeys:
        semester_list = crud.journey_semester.get_by_journey(db=db, id_journey=journey.id)
        all_semester = []
        for semester in semester_list:
            all_semester.append(semester.semester)
        journey.semester_list = all_semester
        all_journeys.append(journey)
    response = schemas.ResponseJourney(**{'count': count, 'data': all_journeys})
    return response


@router.get("/by_id_mention", response_model=List[schemas.Journey])
def read_journey_by_mention(
        db: Session = Depends(deps.get_db),
        *,
        id_mention: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve journey.
    """
    journeys = crud.journey.get_by_mention(db=db, id_mention=id_mention)
    all_journeys = []
    for journey in journeys:
        semester_list = crud.journey_semester.get_by_journey(db=db, id_journey=journey.id)
        all_semester = []
        for semester in semester_list:
            all_semester.append(semester.semester)
        journey.semester_list = all_semester
        all_journeys.append(journey)
    return all_journeys


@router.post("/", response_model=schemas.Journey)
def create_journey(
        *,
        db: Session = Depends(deps.get_db),
        journey_in: schemas.JourneyCreate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new journey.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    journey = crud.journey.create(db=db, obj_in=journey_in)
    if journey:
        for sems in journey_in.semester:
            journey_semester_in = schemas.JourneySemesterCreate(
                id_journey=journey.id, semester=sems
            )
            crud.journey_semester.create(db=db, obj_in=journey_semester_in)
    semester_list = crud.journey_semester.get_by_journey(db=db, id_journey=journey.id)
    all_semester = []
    for semester in semester_list:
        all_semester.append(semester.semester)
    journey.semester_list = all_semester
    return journey


@router.get("/by_id/", response_model=schemas.Journey)
def read_journey_by_id(
        *,
        db: Session = Depends(deps.get_db),
        id_journey: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get journey by ID.
    """
    journey = crud.journey.get_by_id(db=db, id=id_journey)
    if not journey:
        raise HTTPException(status_code=404, detail="journey not found")
    semester_list = crud.journey_semester.get_by_journey(db=db, id_journey=id_journey)
    all_semester = []
    for semester in semester_list:
        all_semester.append(semester.semester)
    journey.semester_list = all_semester
    return journey


@router.delete("/", response_model=schemas.Journey)
def delete_journey(
        *,
        db: Session = Depends(deps.get_db),
        id_journey: str,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an journey.
    """
    journey = crud.journey.get(db=db, id=id_journey)
    if not journey:
        raise HTTPException(status_code=404, detail="journey not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    journey = crud.journey.remove(db=db, id=id_journey)
    return journey
