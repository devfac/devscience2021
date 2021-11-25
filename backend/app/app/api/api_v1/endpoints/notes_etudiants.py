from typing import Any, List

import sqlalchemy

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.db.session import engine
from sqlalchemy.sql.ddl import CreateSchema
from app.utils import create_anne
from app.core.config import settings

router = APIRouter()

@router.post("/insert_etudiants", response_model=List[Any])
def inserts_etudiant(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semstre:str,
    parcours:str,
    uuid_parcours:str,
    uuid_mention:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """ 
    etudiants = []
    list = crud.ancien_etudiant.get_by_class(schemas,uuid_parcours,uuid_mention,semstre)
    if list is not None:
        for etudiant in list:
            et_un = crud.note.read_by_num_carte(schemas, semstre, parcours,etudiant.num_carte)
            if not et_un:
                crud.note.insert_note(schemas,semstre,parcours,etudiant.num_carte)
    etudiants = crud.note.read_all_note(schemas, semstre, parcours)
    return etudiants


@router.post("/insert_note", response_model=List[Any])
def inserts_note(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre: str,
    parcours:str,
    uuid_parcours:str,
    note:schemas.MatierUni,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """ 


@router.delete("/", response_model=schemas.Msg)
def delete_table_note(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre: str,
    parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
   
    if crud.user.is_superuser(current_user):
        test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours)
        if test_note:
            if models.note.drop_table_note(schemas=schemas,parcours=parcours,semestre=semestre):
                return {"msg":"Succces"}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error")
        else:
            raise HTTPException(
            status_code=400,
            detail=f"note_{semestre}_{parcours} not found.",
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
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours)
    if test_note:
        return crud.note.check_columns_exist(schemas=schemas, semestre=semestre,parcours=parcours)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"note_{semestre}_{parcours} not found.",
        )
