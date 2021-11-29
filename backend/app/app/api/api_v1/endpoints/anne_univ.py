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


@router.get("/", response_model=List[schemas.AnneUniv])
def read_annee_universitaire(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve anne universitaire.
    """
    anne_univ = crud.anne_univ.get_multi(db, skip=skip, limit=limit)
    return anne_univ
    


@router.post("/", response_model=schemas.AnneUniv)
def create_annee_universitaire(
    *,
    db: Session = Depends(deps.get_db),
    anne_univ_in: schemas.AnneUnivCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new anne universitaire.
    """
   
    if crud.user.is_superuser(current_user):
        anne_univ = crud.anne_univ.get_by_title(db, title=anne_univ_in.title)
        if not anne_univ:
            anne_univ = crud.anne_univ.create(db=db, obj_in=anne_univ_in)
            try:
                schem_et = create_anne(anne_univ.title)
                engine.execute(CreateSchema(schem_et))
                models.etudiant.create(schem_et)
                reponse = "Success"
            except sqlalchemy.exc.ProgrammingError:
                reponse = "Erreur"
        else:
            raise HTTPException(
            status_code=400,
            detail=f"{anne_univ.title} already exists in the system.",
        )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return anne_univ


@router.put("/", response_model=schemas.AnneUniv)
def update_annee_universitaire(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    anne_univ_in: schemas.AnneUnivUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an anne universitaire.
    """
    anne_univ = crud.anne_univ.get_by_uuid(db=db, uuid=uuid)
    if not anne_univ:
        raise HTTPException(status_code=404, detail="Anne Univ not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    anne_univ = crud.semetre.update(db=db, db_obj=anne_univ, obj_in=anne_univ_in)
    return anne_univ


@router.get("/by_uuid", response_model=schemas.AnneUniv)
def read_annee_universitaire(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get anne universitaire by ID.
    """
    anne_univ = crud.anne_univ.get_by_uuid(db=db, uuid=uuid)
    if not anne_univ:
        raise HTTPException(status_code=404, detail="Anne Univ not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return anne_univ


@router.delete("/", response_model=schemas.AnneUniv)
def delete_annee_universitaire(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete anne universitaire.
    """
    anne_univ = crud.anne_univ.get_by_uuid(db=db, uuid=uuid)
    if not anne_univ:
        raise HTTPException(status_code=404, detail="Anne Univ not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    anne_univ = crud.semetre.remove_uuid(db=db, uuid=uuid)
    return anne_univ
