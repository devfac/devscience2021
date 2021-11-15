from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SemestreValide])
def read_semestres_valides(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve semetres valides.
    """
    if crud.user.is_superuser(current_user):
        semetre_valide = crud.semetre_valide.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return semetre_valide


@router.post("/", response_model=schemas.SemestreValide)
def create_semestre_valide(
    *,
    db: Session = Depends(deps.get_db),
    semetre_valide_in: schemas.SemestreValideCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new semetre valide.
    """
    semetre_valide = crud.semetre_valide.create(db=db, obj_in=semetre_valide_in)
    
    return semetre_valide


@router.put("/{num_carte}", response_model=schemas.SemestreValide)
def update_semestre_valide(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    semetre_valide_in: schemas.SemestreValideUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an semetre valide.
    """
    semetre_valide = crud.semetre_valide.get_by_num_carte(db=db, num_carte=num_carte)
    if not semetre_valide:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    semetre_valide = crud.semetre.update(db=db, db_obj=semetre_valide, obj_in=semetre_valide_in)
    return semetre_valide


@router.get("/{num_carte}", response_model=schemas.SemestreValide)
def read_semestre(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get semetre valide by Numero carte.
    """
    semetre_valide = crud.semetre_valide.get_by_num_carte(db=db, num_carte=num_carte)
    if not semetre_valide:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return semetre_valide


@router.delete("/{uuid}", response_model=schemas.SemestreValide)
def delete_semestre_valide(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an semetre valide.
    """
    semetre_valide = crud.semetre_valide.get_by_num_carte(db=db, num_carte=num_carte)
    if not semetre_valide:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    
    semetre_valide = crud.semetre_valide.remove_uuid(db=db, uuid=semetre_valide.uuid)
    return semetre_valide
