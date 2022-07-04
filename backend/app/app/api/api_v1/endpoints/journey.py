from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Journey])
def read_journey(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve paarcours.
    """
    journey = crud.journey.get_multi(db=db)
    return journey


@router.post("/", response_model=List[schemas.Journey])
def create_journey(
    *,
    db: Session = Depends(deps.get_db),
    paarcours_in: schemas.JourneyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new journey.
    """
    if crud.user.is_superuser(current_user):
        journey = crud.journey.create(db=db, obj_in=paarcours_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.journey.get_multi(db=db)


@router.put("/", response_model=List[schemas.Journey])
def update_journey(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    journey_in: schemas.JourneyUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an journey.
    """
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid)
    if not journey:
        raise HTTPException(status_code=404, detail="Mention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    journey = crud.mention.update(db=db, db_obj=journey, obj_in=journey_in)
    return crud.journey.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Journey)
def read_journey_by_uuid(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get journey by ID.
    """
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid)
    if not journey:
        raise HTTPException(status_code=404, detail="journey not found")
    return journey


@router.get("/by_mention/", response_model=List[schemas.Journey])
def read_journey_by_mention(
    *,
    db: Session = Depends(deps.get_db),
    uuid_mention: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get journey by mention.
    """
    journey = crud.journey.get_by_mention(db=db, uuid_mention=uuid_mention)
    if not journey:
        raise HTTPException(status_code=404, detail="journey not found")
    return journey


@router.delete("/", response_model=List[schemas.Journey])
def delete_journey(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an journey.
    """
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid)
    if not journey:
        raise HTTPException(status_code=404, detail="journey not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    journey = crud.journey.remove_uuid(db=db, uuid=uuid)
    return crud.journey.get_multi(db=db)
