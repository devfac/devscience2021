from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseClassroom)
def read_classroom(
        db: Session = Depends(deps.get_db),
        limit: int = 100,
        offset: int = 0,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve classrooms.
    """
    count = crud.classroom.get_count(db=db)
    classroom = crud.classroom.get_multi(db=db, limit=limit, skip=offset, order_by="name")
    response = schemas.ResponseClassroom(**{'count': count, 'data': classroom})
    return response


@router.get("/by_id", response_model=schemas.Classroom)
def read_classroom(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        id_classroom: int,
) -> Any:
    """
    Retrieve classrooms.
    """
    classroom = crud.classroom.get(db=db, id=id_classroom)
    return classroom


@router.post("/", response_model=List[schemas.Classroom])
def create_classroom(
        *,
        db: Session = Depends(deps.get_db),
        classroom_in: schemas.ClassroomCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new classroom.
    """
    classroom = crud.classroom.get_by_name(db=db, name=classroom_in.name)
    if classroom:
        raise HTTPException(status_code=401, detail="Classroom already exist")

    if crud.user.is_superuser(current_user):
        crud.classroom.create(db=db, obj_in=classroom_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    classroom = crud.classroom.get_multi(db=db, order_by="name")
    return classroom


@router.put("/", response_model=List[schemas.Classroom])
def update_classroom(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        classroom_in: schemas.ClassroomUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an classroom.
    """
    classroom = crud.classroom.get_by_id(db=db, uuid=uuid)
    if not classroom:
        raise HTTPException(status_code=404, detail="classroom not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.classroom.update(db=db, db_obj=classroom, obj_in=classroom_in)
    classroom = crud.classroom.get_multi(db=db, order_by="name")
    return classroom


@router.delete("/", response_model=schemas.Classroom)
def delete_classroom(
        *,
        db: Session = Depends(deps.get_db),
        id_classroom: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an classroom.
    """
    classroom = crud.classroom.get(db=db, id=id_classroom)
    if not classroom:
        raise HTTPException(status_code=404, detail="classroom not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.classroom.remove(db=db, id=id_classroom)
    return classroom
