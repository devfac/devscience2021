from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Validation])
def read_validation(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve semesters valides.
    """
    if crud.user.is_superuser(current_user):
        validation = crud.validation.get_all(db=db)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return validation


@router.post("/", response_model=schemas.Validation)
def create_validation(
        db: Session = Depends(deps.get_db),
        *,
        semester: str,
        college_year: str = "",
        num_carte: str,
        validation_in: schemas.ValidationCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an validation.
    """
    validation = crud.validation.get_by_num_carte(db=db, num_carte=num_carte)
    validation_value = jsonable_encoder(validation_in)
    historic = schemas.HistoricCreate(email=current_user.email,
                                      action=f"{jsonable_encoder(validation_in)}",
                                      title=f"Update validation",
                                      college_year=college_year)
    hist = crud.historic.create(db=db, obj_in=historic)
    if not validation:
        print("eto")
        for i in range(10):
            if f"s{(i + 1)}" != semester.lower():
                validation_value[f"s{(i + 1)}"] = None

        validation_value["num_carte"] = num_carte
        validation = crud.validation.create(db=db, obj_in=validation_value)
    else:
        print("ato")
        new_value = {}
        for data in validation_value:
            if validation_value[data]:
                new_value[data] =validation_value[data] if validation_value[data] != 'null' else None
        value_update = schemas.ValidationUpdate(**new_value)
        validation = crud.validation.get_by_num_carte(db=db, num_carte=num_carte)
        print(jsonable_encoder(validation))
        validation = crud.validation.update(db=db, db_obj=validation, obj_in=value_update)
    return validation


@router.get("/by_num_carte", response_model=schemas.Validation)
def read_validation(
        db: Session = Depends(deps.get_db),
        *,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get validation by Numero carte.
    """
    validation = crud.validation.get_by_num_carte(db=db, num_carte=num_carte)
    if not validation:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    print(jsonable_encoder(validation))
    return validation


@router.delete("/", response_model=List[schemas.Validation])
def delete_validation(
        db: Session = Depends(deps.get_db),
        *,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an validation.
    """
    validation = crud.validation.get_by_num_carte(db=db, num_carte=num_carte)
    if not validation:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    validation = crud.validation.remove_uuid(db=db, uuid=validation.uuid)
    return validation
