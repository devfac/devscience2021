from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Semester])
def read_semesters(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve semesters.
    """
    semester = crud.semester.get_multi(db=db)
    return semester


@router.post("/", response_model=schemas.Semester)
def create_semester(
    *,
    db: Session = Depends(deps.get_db),
    semester_in: schemas.SemesterCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new semester.
    """
    if crud.user.is_superuser(current_user):
        semester = crud.semester.create(db=db, obj_in=semester_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return semester


@router.put("/", response_model=schemas.Semester)
def update_semester(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    semester_in: schemas.SemesterUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an semester.
    """
    semester = crud.semester.get_by_uuid(db=db, uuid=uuid)
    if not semester:
        raise HTTPException(status_code=404, detail="semester not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    semester = crud.semester.update(db=db, db_obj=semester, obj_in=semester_in)
    return semester


@router.get("/", response_model=schemas.Semester)
def read_semester(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get semester by ID.
    """
    semester = crud.semester.get_by_uuid(db=db, uuid=uuid)
    if not semester:
        raise HTTPException(status_code=404, detail="semester not found")
    return semester


@router.delete("/", response_model=schemas.Semester)
def delete_semester(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an semester.
    """
    semester = crud.semester.get_by_uuid(db=db, uuid=uuid)
    if not semester:
        raise HTTPException(status_code=404, detail="semester not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    semester = crud.semester.remove_uuid(db=db, uuid=uuid)
    return semester
