from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.db.session import engine
from sqlalchemy.sql.ddl import CreateSchema
from app.utils import create_anne, compare_list
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=Any)
def create_table_note(
        *,
        db: Session = Depends(deps.get_db),
        schemas: str,
        semestre: str,
        session_: str,
        uuid_parcours: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """

    if crud.user.is_superuser(current_user):
        matiers = []
        parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
        if not parcours:
            raise HTTPException(status_code=400, detail="Parcours not found")

        if semestre not in parcours.semestre:
            raise HTTPException(status_code=400, detail="Semestre not found in parcours")

        ues = crud.matier_ue.get_by_class(schema=schemas, uuid_parcours=uuid_parcours, semestre=semestre)
        for index, ue in enumerate(ues):
            matiers.append("ue_" + ue[2])
            ecs = crud.matier_ec.get_by_value_ue(schema=schemas, value_ue=ue[2], semestre=semestre,
                                                 uuid_parcours=uuid_parcours)
            for index, ec in enumerate(ecs):
                matiers.append("ec_" + ec[2])
        sesions = ["normal", "rattrapage", "final"]
        for session in sesions:
            test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre, parcours=parcours.abreviation,
                                                    session=session)
            if not test_note:
                models.note.create_table_note(schemas=schemas, parcours=parcours.abreviation, semestre=semestre,
                                              matiers=matiers, session=session)
            else:
                all_columns = crud.note.check_columns_exist(schemas=schemas, semestre=semestre,
                                                            parcours=parcours.abreviation, session=session)
                matier = compare_list(matiers, all_columns)
                if len(matier) != 0:
                    models.note.update_table_note(schemas=schemas, parcours=parcours.abreviation, semestre=semestre,
                                                  matiers=matiers, session=session)
                else:
                    return crud.note.check_columns_exist(schemas=schemas, semestre=semestre,
                                                         parcours=parcours.abreviation,
                                                         session=session_.lower())
        test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre, parcours=parcours.abreviation,
                                                session=session_.lower())
        if test_note:
            return crud.note.check_columns_exist(schemas=schemas, semestre=semestre, parcours=parcours.abreviation,
                                                 session=session_.lower())
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.delete("/", response_model=schemas.Msg)
def delete_table_note(
        *,
        db: Session = Depends(deps.get_db),
        schemas: str,
        semestre: str,
        uuid_parcours: str,
        session: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """

    if crud.user.is_superuser(current_user):

        parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
        if not parcours:
            raise HTTPException(status_code=400, detail="Parcours not found")
        test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre, parcours=parcours.abreviation,
                                                session=session)
        if test_note:
            if models.note.drop_table_note(schemas=schemas, parcours=parcours.abreviation, session=session,
                                           semestre=semestre):
                return {"msg": "Succces"}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"note_{parcours.abreviation.lower()}_{semestre.lower()}_{session.lower()} not found.",
            )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.get("/", response_model=Any)
def get_all_columns(
        *,
        db: Session = Depends(deps.get_db),
        schemas: str,
        semestre: str,
        session: str,
        uuid_parcours: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre, parcours=parcours.abreviation,
                                            session=session)
    if test_note:
        return crud.note.check_columns_exist(schemas=schemas, semestre=semestre, parcours=parcours.abreviation,
                                             session=session)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"note_{parcours.abreviation.lower()}_{semestre.lower()}_{session.lower()} not found.",
        )
