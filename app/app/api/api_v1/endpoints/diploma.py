from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Diploma])
def read_diploma(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve semesters valides.
    """
    if crud.user.is_superuser(current_user):
        diploma = crud.diploma.get_all(db=db)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return diploma


@router.post("/", response_model=schemas.Diploma)
def create_diploma(
        db: Session = Depends(deps.get_db),
        *,
        diploma_type: str,
        diploma_in: schemas.DiplomaCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an diploma.
    """
    all_title = {"master":None, "licence":None}
    list_title = ["master", "licence"]
    if diploma_type not in all_title:
        raise HTTPException(status_code=404, detail="diploma type invalid")

    diploma = crud.diploma.get_by_num_carte(
        db=db, num_carte=diploma_in.num_carte)
    diploma_value = jsonable_encoder(diploma_in)

    if not diploma:
        for title in list_title:
            if title != diploma_type.lower():
                diploma_value[f"{title}_title"] = None
        diploma = crud.diploma.create(db=db, obj_in=diploma_value)
    else:
        new_value = {}
        for data in diploma_value:
            if diploma_value[data]:
                new_value[data] = diploma_value[data]

        diploma = crud.interaction.update(db=db, db_obj=diploma, obj_in=new_value)
    return diploma


@router.get("/by_num_carte", response_model=schemas.Diploma)
def read_diploma(
        db: Session = Depends(deps.get_db),
        *,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get diploma by Numero carte.
    """
    diploma = crud.diploma.get_by_num_carte(db=db, num_carte=num_carte)
    if not diploma:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return diploma


@router.delete("/", response_model=List[schemas.Diploma])
def delete_diploma(
        db: Session = Depends(deps.get_db),
        *,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an diploma.
    """
    diploma = crud.diploma.get_by_num_carte(db=db, num_carte=num_carte)
    if not diploma:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    diploma = crud.diploma.remove_id(db=db, uuid=diploma.id)
    return diploma
