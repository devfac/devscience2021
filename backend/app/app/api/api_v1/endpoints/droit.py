from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Droit])
def read_droits(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve droits.
    """
    if crud.user.is_superuser(current_user):
        droit = crud.droit.get_multi(db=db)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return droit


@router.post("/", response_model=schemas.Droit)
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
    return droit


@router.put("/", response_model=schemas.Droit)
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
    droit = crud.droit.update(db=db, db_obj=droit, obj_in=droit_in)
    return droit


@router.get("/by_niveau_and_annee", response_model=schemas.Droit)
def read_droit(
    *,
    db: Session = Depends(deps.get_db),
    uuid_mention: str,
    annee:str,
    niveau:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get droit by ID.
    """
    droit = crud.droit.get_by_niveau_and_annee(db=db,niveau=niveau,annee=annee,uuid_mention=uuid_mention)
    if not droit:
        raise HTTPException(status_code=404, detail="droit not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return droit


@router.delete("/", response_model=schemas.Droit)
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
    droit = crud.droit.remove_uuid(db=db, uuid=uuid)
    return droit
