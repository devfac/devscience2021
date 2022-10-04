from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SemesterValide])
def read_semesters_valides(
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve semesters valides.
    """
    if crud.user.is_superuser(current_user):
        semester_valide = crud.semester_valide.get_all(schema=schema)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return semester_valide


@router.post("/", response_model=schemas.SemesterValide)
def update_semester_valide(
        schema: str,
        semester_valide_in: schemas.SemesterValideCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an semester valide.
    """
    semester_valide = crud.semester_valide.get_by_num_carte(schema=schema, num_carte=semester_valide_in.num_carte)
    if not semester_valide:
        semester_valide_in.uuid = uuid.uuid4()
        semester_valide = crud.semester_valide.create_sems(schema=schema, obj_in=semester_valide_in)
    else:
        semester_ = []
        for sems_val in semester_valide_in.semester:
            if sems_val not in semester_valide.semester:
                semester_.append(sems_val)
            else:
                semester_valide.semester.remove(sems_val)

        semester_valide_in.semester = semester_valide.semester + semester_
        if len(semester_valide_in.semester) != 0:
            sems = {"semester": semester_valide_in.semester}
            semester_valide = crud.semester_valide.update_sems(schema=schema, obj_in=sems,
                                                              num_carte=semester_valide_in.num_carte)
        else:
            semester_valide = crud.semester_valide.delete_sems(schema=schema, num_carte=semester_valide_in.num_carte)
    return semester_valide


@router.get("/by_num_carte", response_model=schemas.SemesterValide)
def read_semester(
        schema: str,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get semester valide by Numero carte.
    """
    semester_valide = crud.semester_valide.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not semester_valide:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return semester_valide


@router.delete("/", response_model=List[schemas.SemesterValide])
def delete_semester_valide(
        schema: str,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an semester valide.
    """
    semester_valide = crud.semester_valide.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not semester_valide:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    semester_valide = crud.semester_valide.delete_sems(schema=schema, num_carte=num_carte)
    return semester_valide
