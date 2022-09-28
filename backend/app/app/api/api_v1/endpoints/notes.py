import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import compare_list, create_anne

from app.script_logging import ScriptLogging

router = APIRouter()


@router.post("/", response_model=Any)
def create_table_note(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        session: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """

    logging_ = ScriptLogging(current_user.email)
    if crud.user.is_superuser(current_user):
        matiers = []
        journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
        if not journey:
            raise HTTPException(status_code=400, detail="journey not found")

        if semester not in journey.semester:
            raise HTTPException(status_code=400, detail="semester not found in journey")

        ues = crud.matier_ue.get_by_class(schema=create_anne(schema), uuid_journey=uuid_journey, semester=semester)
        for index, ue in enumerate(ues):
            matiers.append("ue_" + ue[2])
            ecs = crud.matier_ec.get_by_value_ue(schema=create_anne(schema), value_ue=ue[2], semester=semester,
                                                 uuid_journey=uuid_journey)
            for index_2, ec in enumerate(ecs):
                matiers.append("ec_" + ec[2])
        sesions = ["normal", "rattrapage", "final"]
        for session in sesions:
            test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                                    session=session)
            print(test_note)
            if not test_note:
                models.note.create_table_note(schema=create_anne(schema), journey=journey.abbreviation, semester=semester,
                                              matiers=matiers, session=session)
            else:
                all_columns = crud.note.check_columns_exist(schema=create_anne(schema), semester=semester,
                                                            journey=journey.abbreviation, session=session)
                matier = compare_list(matiers, all_columns)
                if len(matier) != 0:
                    models.note.update_table_note(schema=create_anne(schema), journey=journey.abbreviation, semester=semester,
                                                  matiers=matiers, session=session)
                else:
                    return crud.note.check_columns_exist(schema=create_anne(schema), semester=semester,
                                                         journey=journey.abbreviation,
                                                         session=session.lower())
        test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                                session=session.lower())
        if test_note:
            return crud.note.check_columns_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                                 session=session.lower())

    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.delete("/", response_model=schemas.Msg)
def delete_table_note(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        uuid_journey: str,
        session: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
    if crud.user.is_superuser(current_user):

        journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
        if not journey:
            raise HTTPException(status_code=400, detail="journey not found")
        test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                                session=session)
        if test_note:
            if models.note.drop_table_note(schema=create_anne(schema), journey=journey.abbreviation, session=session,
                                           semester=semester):
                return {"msg": "Succces"}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
            )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.get("/", response_model=Any)
def get_all_columns(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        session: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                            session=session)
    if test_note:
        return crud.note.check_columns_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                             session=session)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
        )
