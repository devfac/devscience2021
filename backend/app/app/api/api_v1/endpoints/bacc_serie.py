from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import decode_text

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_bacc_series(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve bacc_series.
    """
    if crud.user.is_superuser(current_user):
        bacc_serie = crud.bacc_serie.get_multi(db=db)
        count = len(crud.bacc_serie.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':bacc_serie})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.BaccSerie])
def create_bacc_serie(
    *,
    db: Session = Depends(deps.get_db),
    bacc_serie_in: schemas.BaccSerieCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new bacc_serie.
    """
    value = decode_text(bacc_serie_in.title).lower()
    if crud.user.is_superuser(current_user):
        bacc_serie = crud.bacc_serie.create(db=db, obj_in=bacc_serie_in, value=value)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.bacc_serie.get_multi(db=db)


@router.put("/", response_model=List[schemas.BaccSerie])
def update_bacc_serie(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    bacc_serie_in: schemas.BaccSerieUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an bacc_serie.
    """
    bacc_serie = crud.bacc_serie.get_by_uuid(db=db, uuid=uuid)
    if not bacc_serie:
        raise HTTPException(status_code=404, detail="BaccSerie not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bacc_serie = crud.bacc_serie.update(db=db, db_obj=bacc_serie, obj_in=bacc_serie_in)
    return crud.bacc_serie.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.BaccSerie)
def read_bacc_serie(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get bacc_serie by ID.
    """
    bacc_serie = crud.bacc_serie.get_by_uuid(db=db, uuid=uuid)
    if not bacc_serie:
        raise HTTPException(status_code=404, detail="BaccSerie not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return bacc_serie


@router.delete("/", response_model=List[schemas.BaccSerie])
def delete_bacc_serie(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an bacc_serie.
    """
    bacc_serie = crud.bacc_serie.get_by_uuid(db=db, uuid=uuid)
    if not bacc_serie:
        raise HTTPException(status_code=404, detail="BaccSerie not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bacc_serie = crud.bacc_serie.remove_uuid(db=db, uuid=uuid)
    return crud.bacc_serie.get_multi(db=db)
