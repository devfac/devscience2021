from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Semestre])
def read_semestres(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve semetres.
    """
    if crud.user.is_superuser(current_user):
        semetre = crud.semetre.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return semetre


@router.post("/", response_model=schemas.Semestre)
def create_semestre(
    *,
    db: Session = Depends(deps.get_db),
    semetre_in: schemas.SemestreCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new semetre.
    """
    if crud.user.is_superuser(current_user):
        semetre = crud.semetre.create(db=db, obj_in=semetre_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return semetre


@router.put("/", response_model=schemas.Semestre)
def update_semestre(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    semetre_in: schemas.SemestreUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an semetre.
    """
    semetre = crud.semetre.get_by_uuid(db=db, uuid=uuid)
    if not semetre:
        raise HTTPException(status_code=404, detail="Semestre not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    semetre = crud.semetre.update(db=db, db_obj=semetre, obj_in=semetre_in)
    return semetre


@router.get("/", response_model=schemas.Semestre)
def read_semestre(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get semetre by ID.
    """
    semetre = crud.semetre.get_by_uuid(db=db, uuid=uuid)
    if not semetre:
        raise HTTPException(status_code=404, detail="Semestre not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return semetre


@router.delete("/", response_model=schemas.Semestre)
def delete_semestre(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an semestre.
    """
    semetre = crud.semetre.get_by_uuid(db=db, uuid=uuid)
    if not semetre:
        raise HTTPException(status_code=404, detail="Semestre not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    semetre = crud.semetre.remove_uuid(db=db, uuid=uuid)
    return semetre
