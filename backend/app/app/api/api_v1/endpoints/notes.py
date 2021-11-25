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

@router.post("/", response_model=schemas.Msg)
def create_table_note(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre: str,
    parcours:str,
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
   
    if crud.user.is_superuser(current_user):
        test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours)
        if not test_note:
            print('blallablabla')
            matiers = []
            ues = crud.matier_ue.get_by_class(schema=schemas, uuid_parcours=uuid_parcours, semestre=semestre)
            for index ,ue in enumerate(ues):
                matiers.append("ue_"+ue[2])
                print(ue[2])
                ecs = crud.matier_ec.get_by_value_ue(schema=schemas, value_ue=ue[2],semestre=semestre,uuid_parcours=uuid_parcours)
                for index,ec in enumerate(ecs):
                    matiers.append("ec_"+ec[2])
                    print(ec[2])
            print(ues)
            if models.note.create_table_note(schemas=schemas,parcours=parcours,semestre=semestre,matiers=matiers):
                return {"msg":"Succces"}
            else:
                return {"msg":"Error"}
        else:
            raise HTTPException(
            status_code=400,
            detail=f"note_{semestre}_{parcours} already exists in the system.",
        )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
 