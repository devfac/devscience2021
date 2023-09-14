from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_model=schemas.ValidationUpdate)
def create_validation(
        db: Session = Depends(deps.get_db),
        *,
        semester: str,
        num_carte: str,
        session: str,
        uuid_journey: str,
        validation_in: schemas.ValidationNoteUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an validation.
    """

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    et_un = crud.note.read_by_num_carte(semester=semester, journey=journey.abbreviation,
                                        session=session, num_carte=num_carte)

    validation_in = jsonable_encoder(validation_in)
    if et_un:
        crud.note.update_note(semester, journey.abbreviation, session, num_carte, validation_in)
        crud.note.update_note(semester, journey.abbreviation, "final", num_carte, validation_in)

        validation = crud.validation.get_by_num_carte_and_semester_and_journey(
            db=db, num_carte=num_carte, semester=semester, uuid_journey=uuid_journey)
        if validation_in['validation']:
            if not validation:
                validation_schema = schemas.ValidationCreate(semester=semester, num_carte=num_carte, session=session,
                                                             uuid_journey=uuid_journey, mean=et_un.mean,
                                                             credit=et_un.credit, year=et_un.year)
                crud.validation.create(db=db, obj_in=validation_schema)
        else:
            if validation:
                crud.validation.remove_uuid(db=db, uuid=validation.uuid)
    else:
        raise HTTPException(status_code=400, detail="Student not found")
    return et_un


@router.get("/by_uuid/", response_model=schemas.Validation)
def read_validation(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get validation by ID.
    """
    validation = crud.validation.get_by_uuid(db=db, uuid=uuid)
    if not validation:
        raise HTTPException(status_code=404, detail="Validation not found")
    return validation


@router.get("/by_num_carte/{num_carte}", response_model=List[schemas.Validation])
def read_validation(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get validation by ID.
    """
    validation = crud.validation.get_by_num_carte(db=db, num_carte=num_carte)
    return validation


@router.get("/by_journey/{uuid_journey}", response_model=List[schemas.Validation])
def read_validation(
    *,
    db: Session = Depends(deps.get_db),
    uuid_journey: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get validation by ID.
    """
    validation = crud.validation.get_by_journey(db=db, uuid_journey=uuid_journey)
    return validation
