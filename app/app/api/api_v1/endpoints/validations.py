from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_validations(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve validations.
    """
    validation = crud.validation.get_multi(db=db)
    count = len(crud.validation.get_count(db=db))
    response = schemas.ResponseData(**{'count':count, 'data':validation})
    return response


@router.post("/", response_model=List[schemas.Validation])
def create_validation(
    *,
    db: Session = Depends(deps.get_db),
    validation_in: schemas.ValidationCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new validation.
    """
    validation = crud.validation.create(db=db, obj_in=validation_in)


@router.put("/", response_model=List[schemas.Validation])
def update_validation(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    validation_in: schemas.ValidationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an validation.
    """
    validation = crud.validation.get_by_id(db=db, uuid=uuid)
    if not validation:
        raise HTTPException(status_code=404, detail="Validation not found")
    validation = crud.validation.update(db=db, db_obj=validation, obj_in=validation_in)
    return crud.validation.get_multi(db=db)


@router.get("/by_id/", response_model=schemas.Validation)
def read_validation(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get validation by ID.
    """
    validation = crud.validation.get_by_id(db=db, uuid=uuid)
    if not validation:
        raise HTTPException(status_code=404, detail="Validation not found")
    return validation


@router.delete("/", response_model=List[schemas.Validation])
def delete_validation(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an validation.
    """
    validation = crud.validation.get_by_id(db=db, uuid=uuid)
    if not validation:
        raise HTTPException(status_code=404, detail="Validation not found")
    validation = crud.validation.remove_id(db=db, uuid=uuid)
    return crud.validation.get_multi(db=db)
