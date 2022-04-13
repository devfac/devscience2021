from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Diplome])
def read_diplome(
    schema:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve semetres valides.
    """
    if crud.user.is_superuser(current_user):
        diplome = crud.diplome.get_all(schema=schema)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return diplome


@router.post("/", response_model=List[schemas.Diplome])
def create_diplome(
    schema:str,
    diplome_in: schemas.DiplomeCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new semetre valide.
    """
    diplome_in.uuid = uuid.uuid4()
    diplome = crud.diplome.create_diplome(schema=schema, obj_in=diplome_in)
    return diplome


@router.put("/", response_model=List[schemas.Diplome])
def update_diplome(
    schema:str,
    num_carte: str,
    diplome_in: schemas.DiplomeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an semetre valide.
    """
    diplome = crud.diplome.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not diplome:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    diplome = crud.diplome.update_diplome(schema=schema, obj_in=diplome_in, num_carte=num_carte)
    return diplome


@router.get("/by_num_carte", response_model=schemas.Diplome)
def read_diplome(
    schema:str,
    num_carte: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get semetre valide by Numero carte.
    """
    diplome = crud.diplome.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not diplome:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return diplome


@router.get("/by_mention", response_model=List[schemas.Diplome])
def read_diplome(
    schema:str,
    uuid_mention: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get semetre valide by Numero carte.
    """

    mention = crud.mention.get_by_uuid(db = db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.",)
    diplome = crud.diplome.get_by_mention(schema=schema, uuid_mention=uuid_mention)

    if not diplome:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return diplome


@router.delete("/", response_model=List[schemas.Diplome])
def delete_diplome(
    schema:str,
    num_carte: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an semetre valide.
    """
    diplome = crud.diplome.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not diplome:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    
    diplome = crud.diplome.delete_diplome(schema=schema, num_carte=num_carte)
    return diplome
