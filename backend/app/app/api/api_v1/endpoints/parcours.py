import json
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.utils import UUIDEncoder

router = APIRouter()


@router.get("/", response_model=List[schemas.Parcours])
def read_parcours(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve paarcours.
    """
    parcours = crud.parcours.get_multi(db=db)
    return parcours


@router.post("/", response_model=List[schemas.Parcours])
def create_parcours(
    *,
    db: Session = Depends(deps.get_db),
    paarcours_in: schemas.ParcoursCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new parcours.
    """
    if crud.user.is_superuser(current_user):
        parcours = crud.parcours.create(db=db, obj_in=paarcours_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.parcours.get_multi(db=db)


@router.put("/", response_model=List[schemas.Parcours])
def update_parcours(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    parcours_in: schemas.ParcoursUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an parcours.
    """
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid)
    if not parcours:
        raise HTTPException(status_code=404, detail="Mention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    parcours = crud.mention.update(db=db, db_obj=parcours, obj_in=parcours_in)
    return crud.parcours.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Parcours)
def read_parcours_by_uuid(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get parcours by ID.
    """
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid)
    if not parcours:
        raise HTTPException(status_code=404, detail="Parcours not found")
    return parcours


@router.get("/by_mention/", response_model=List[schemas.Parcours])
def read_parcours_by_mention(
    *,
    db: Session = Depends(deps.get_db),
    uuid_mention: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get parcours by mention.
    """
    parcours = crud.parcours.get_by_mention(db=db, uuid_mention=uuid_mention)
    if not parcours:
        raise HTTPException(status_code=404, detail="Parcours not found")
    return parcours


@router.delete("/", response_model=List[schemas.Parcours])
def delete_parcours(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an parcours.
    """
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid)
    if not parcours:
        raise HTTPException(status_code=404, detail="Parcours not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    parcours = crud.parcours.remove_uuid(db=db, uuid=uuid)
    return crud.parcours.get_multi(db=db)
