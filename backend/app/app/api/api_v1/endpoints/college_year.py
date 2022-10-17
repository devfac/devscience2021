from typing import Any, List

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.ddl import CreateSchema

from app import crud, models, schemas
from app.api import deps
from app.db.session import engine
from app.utils import create_anne

router = APIRouter()


@router.get("/", response_model=List[schemas.CollegeYear])
def read_college_year(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve anne universitaire.
    """
    college_year = crud.college_year.get_multi(db)
    return college_year


@router.post("/", response_model=List[schemas.CollegeYear])
def create_college_year(
        *,
        db: Session = Depends(deps.get_db),
        college_year_in: schemas.CollegeYearCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new anne universitaire.
    """

    if crud.user.is_superuser(current_user):
        college_year = crud.college_year.get_by_title(db, title=college_year_in.title)
        if not college_year:
            crud.college_year.create(db=db, obj_in=college_year_in)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"{college_year.title} already exists in the system.",
            )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.college_year.get_multi(db=db)


@router.put("/", response_model=List[schemas.CollegeYear])
def update_college_year(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        college_year_in: schemas.CollegeYearUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an anne universitaire.
    """
    college_year = crud.college_year.get_by_uuid(db=db, uuid=uuid)
    if not college_year:
        raise HTTPException(status_code=404, detail="Anne Univ not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    college_year = crud.college_year.update(db=db, db_obj=college_year, obj_in=college_year_in)
    return crud.college_year.get_multi(db=db)


@router.get("/{uuid}", response_model=schemas.CollegeYear)
def read_college_year(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get anne universitaire by ID.
    """

    college_year = crud.college_year.get_by_uuid(db=db, uuid=uuid)
    if not college_year:
        raise HTTPException(status_code=404, detail="Anne Univ not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return college_year


@router.delete("/", response_model=List[schemas.CollegeYear])
def delete_college_year(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete anne universitaire.
    """
    college_year = crud.college_year.get_by_uuid(db=db, uuid=uuid)
    if not college_year:
        raise HTTPException(status_code=404, detail="Anne Univ not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    college_year = crud.college_year.remove_uuid(db=db, uuid=uuid)
    return crud.college_year.get_multi(db=db)
