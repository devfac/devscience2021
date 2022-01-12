from os import SEEK_HOLE
from typing import Any, List
import uuid

from sqlalchemy.sql import schema

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import decode_schemas

router = APIRouter()


@router.get("/", response_model=List[Any])
def read_etudiant_nouveau(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve etudiant nouveau.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",
        )
    etudiant = crud.nouveau_etudiant.get_all(schema=schema)
   
    return etudiant


@router.post("/", response_model=List[schemas.SelectEtudiantBase])
def create_select_etudiant_nouveau(
    *,
    db: Session = Depends(deps.get_db),
    etudiant_in: schemas.SelectEtudiantBase,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new etudiant.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
        
    etudiant_in.uuid = uuid.uuid4()
    etudiant = crud.nouveau_etudiant.create_etudiant(schema=schema, obj_in=etudiant_in)
    return etudiant


@router.put("/update_etudiant/", response_model=List[Any])
def update_etudiant(
    *,
    db: Session = Depends(deps.get_db),
    num_insc: str,
    schema: str,
    etudiant_in: schemas.EtudiantNouveauUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an etudiant.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
        
    etudiant = crud.nouveau_etudiant.get_by_num_insc(schema=schema, num_insc=num_insc)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    etudiant = crud.nouveau_etudiant.update_etudiant(schema=schema,num_insc=num_insc, obj_in=etudiant_in)
    return etudiant


@router.put("/update_etudiant_by_num_select/", response_model=List[Any])
def update_etudiant(
    *,
    db: Session = Depends(deps.get_db),
    num_select: str,
    schema: str,
    etudiant_in: schemas.EtudiantNouveauUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an etudiant.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
        
    etudiant = crud.nouveau_etudiant.get_by_num_select(schema=schema, num_select=num_select)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    etudiant = crud.nouveau_etudiant.update_etudiant_select(schema=schema,num_select=num_select, obj_in=etudiant_in)
    return etudiant



@router.get("/by_num_insc/", response_model=Any)
def read_etudiant_by_num_carte(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    num_insc: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by num insription.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    etudiant = crud.nouveau_etudiant.get_by_num_insc(schema=schema, num_insc=num_insc)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return etudiant

@router.get("/by_mention/", response_model=List[Any])
def read_etudiant_by_mention(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    uuid_mention: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by mention.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    etudiant = crud.nouveau_etudiant.get_by_mention(schema=schema, uuid_mention=uuid_mention)
    
    return etudiant

@router.get("/by_parcours/", response_model=List[Any])
def read_etudiant_by_mention(
    *,
    db: Session = Depends(deps.get_db),
    schema: str,
    uuid_parcours: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by parcours.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    etudiant = crud.nouveau_etudiant.get_by_parcours(schema=schema, uuid_parcours=uuid_parcours)
    return etudiant


@router.delete("/", response_model=List[Any])
def delete_etudiant_nouveau(
    *,
    db: Session = Depends(deps.get_db),
    num_insc: str,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an etudiant.
    """
    anne_univ = crud.anne_univ.get_by_title(db,decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException( status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",)
    etudiant = crud.nouveau_etudiant.get_by_num_insc(schema=schema, num_insc=num_insc)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    etudiant = crud.nouveau_etudiant.delete_etudiant(schema=schema, num_insc=num_insc)
    return etudiant
