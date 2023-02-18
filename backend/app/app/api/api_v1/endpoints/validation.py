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
        validation_in: schemas.ValidationUpdate,
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
    else:
        raise HTTPException(status_code=400, detail="Student not found")
    return et_un