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

@router.post("/", response_model=schemas.Msg)
def create_table_note(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre: str,
    parcours:str,
    session:str,
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
   
    if crud.user.is_superuser(current_user):
        matiers = []
        ues = crud.matier_ue.get_by_class(schema=schemas, uuid_parcours=uuid_parcours, semestre=semestre)
        for index ,ue in enumerate(ues):
            matiers.append("ue_"+ue[2])
            ecs = crud.matier_ec.get_by_value_ue(schema=schemas, value_ue=ue[2],semestre=semestre,uuid_parcours=uuid_parcours)
            for index,ec in enumerate(ecs):
                matiers.append("ec_"+ec[2])
        test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours,session=session)
        if not test_note:
            if models.note.create_table_note(schemas=schemas,parcours=parcours,semestre=semestre,matiers=matiers, session=session):
               models.note.create_table_note(schemas=schemas,parcours=parcours,semestre=semestre,matiers=matiers, session="final")
               return {"msg":"Succces"}
            else:
                return {"msg":"Error"}
        else:
            all_columns = crud.note.check_columns_exist(schemas=schemas, semestre=semestre,parcours=parcours,session=session)
            matiers = compare_list(matiers,all_columns)
            if len(matiers) != 0:
                models.note.update_table_note(schemas=schemas,parcours=parcours,semestre=semestre,matiers=matiers, session=session)
                models.note.update_table_note(schemas=schemas,parcours=parcours,semestre=semestre,matiers=matiers, session="final")

    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.delete("/", response_model=schemas.Msg)
def delete_table_note(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre: str,
    parcours:str,
    session:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
   
    if crud.user.is_superuser(current_user):
        test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours)
        if test_note:
            if models.note.drop_table_note(schemas=schemas,parcours=parcours,session=session,semestre=semestre):
                return {"msg":"Succces"}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error")
        else:
            raise HTTPException(
            status_code=400,
            detail=f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()} not found.",
        )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
 

@router.get("/", response_model=Any)
def get_all_columns(
     *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre: str,
    parcours:str,
    session:str,
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours,session=session)
    if test_note:
        return crud.note.check_columns_exist(schemas=schemas, semestre=semestre,parcours=parcours,session=session)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()} not found.",
        )
