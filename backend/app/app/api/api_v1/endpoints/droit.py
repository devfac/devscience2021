from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Droit])
def read_droit(
    db: Session = Depends(deps.get_db),
        limit: int = 100,
        offset: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve droits.
    """
    droit = crud.droit.get_multi(db=db, limit=limit, skip=offset, order_by="level")
    all_droit = []
    for one_droit in droit:
        mention = crud.mention.get_by_uuid(db=db, uuid=one_droit.uuid_mention)
        droit_ = schemas.Droit(**jsonable_encoder(one_droit), mention=mention)
        all_droit.append(droit_)
    return all_droit


@router.get("/by_mention", response_model=List[schemas.Droit])
def read_droit(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    uuid_mention: str,
    year: str,
) -> Any:
    """
    Retrieve droits.
    """
    droit = crud.droit.get_by_mention_and_year(db=db, uuid_mention=uuid_mention, year=year)
    return droit

@router.get("/by_uuid", response_model=schemas.Droit)
def read_droit(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    uuid: str,
) -> Any:
    """
    Retrieve droits.
    """
    droit = crud.droit.get_by_uuid(db=db, uuid=uuid)
    mention = crud.mention.get_by_uuid(db=db, uuid=droit.uuid_mention)
    droit_ = schemas.Droit(**jsonable_encoder(droit), mention=mention)
    return droit_

@router.post("/", response_model=List[schemas.Droit])
def create_droit(
    *,
    db: Session = Depends(deps.get_db),
    droit_in: schemas.DroitCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new droit.
    """
    if crud.user.is_superuser(current_user):
        droit = crud.droit.create(db=db, obj_in=droit_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    droit = crud.droit.get_multi(db=db, order_by="level")
    all_droit = []
    for one_droit in droit:
        mention = crud.mention.get_by_uuid(db=db, uuid=one_droit.uuid_mention)
        droit_ = schemas.Droit(**jsonable_encoder(one_droit), mention=mention)
        all_droit.append(droit_)
    return all_droit


@router.put("/", response_model=List[schemas.Droit])
def update_droit(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    droit_in: schemas.DroitUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an droit.
    """
    droit = crud.droit.get_by_uuid(db=db, uuid=uuid)
    if not droit:
        raise HTTPException(status_code=404, detail="droit not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.droit.update(db=db, db_obj=droit, obj_in=droit_in)
    droit = crud.droit.get_multi(db=db, order_by="level")
    all_droit = []
    for one_droit in droit:
        mention = crud.mention.get_by_uuid(db=db, uuid=one_droit.uuid_mention)
        droit_ = schemas.Droit(**jsonable_encoder(one_droit), mention=mention)
        all_droit.append(droit_)
    return all_droit


@router.get("/by_level_and_year", response_model=schemas.Droit)
def read_droit(
    *,
    db: Session = Depends(deps.get_db),
    uuid_mention: str,
    year:str,
    level:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get droit by ID.
    """
    droit = crud.droit.get_by_level_and_year(db=db, level=level, year=year, uuid_mention=uuid_mention)
    if not droit:
        raise HTTPException(status_code=404, detail="droit not found")
    return droit


@router.delete("/", response_model=List[schemas.Droit])
def delete_droit(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an droit.
    """
    droit = crud.droit.get_by_uuid(db=db, uuid=uuid)
    if not droit:
        raise HTTPException(status_code=404, detail="droit not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.droit.remove_uuid(db=db, uuid=uuid)
    droit = crud.droit.get_multi(db=db, order_by="level")
    all_droit = []
    for one_droit in droit:
        mention = crud.mention.get_by_uuid(db=db, uuid=one_droit.uuid_mention)
        droit_ = schemas.Droit(**jsonable_encoder(one_droit), mention=mention)
        all_droit.append(droit_)
    return all_droit
