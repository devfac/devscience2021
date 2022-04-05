from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SemestreValide])
def read_semestres_valides(
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve semetres valides.
    """
    if crud.user.is_superuser(current_user):
        semetre_valide = crud.semetre_valide.get_all(schema=schema)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return semetre_valide


@router.post("/", response_model=schemas.SemestreValide)
def update_semestre_valide(
        schema: str,
        semetre_valide_in: schemas.SemestreValideCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an semetre valide.
    """
    semetre_valide = crud.semetre_valide.get_by_num_carte(schema=schema, num_carte=semetre_valide_in.num_carte)
    if not semetre_valide:
        semetre_valide_in.uuid = uuid.uuid4()
        semestre_valide = crud.semetre_valide.create_sems(schema=schema, obj_in=semetre_valide_in)
    else:
        semestre_ = []
        for sems_val in semetre_valide_in.semestre:
            if sems_val not in semetre_valide.semestre:
                semestre_.append(sems_val)
            else:
                semetre_valide.semestre.remove(sems_val)

        semetre_valide_in.semestre = semetre_valide.semestre + semestre_
        if len(semetre_valide_in.semestre) != 0:
            sems = {"semestre": semetre_valide_in.semestre}
            semestre_valide = crud.semetre_valide.update_sems(schema=schema, obj_in=sems,
                                                              num_carte=semetre_valide_in.num_carte)
        else:
            semestre_valide = crud.semetre_valide.delete_sems(schema=schema, num_carte=semetre_valide_in.num_carte)
    return semestre_valide


@router.get("/by_num_carte", response_model=schemas.SemestreValide)
def read_semestre(
        schema: str,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get semetre valide by Numero carte.
    """
    semetre_valide = crud.semetre_valide.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not semetre_valide:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return semetre_valide


@router.delete("/", response_model=List[schemas.SemestreValide])
def delete_semestre_valide(
        schema: str,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an semetre valide.
    """
    semestre_valide = crud.semetre_valide.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not semestre_valide:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    semestre_valide = crud.semetre_valide.delete_sems(schema=schema, num_carte=num_carte)
    return semestre_valide
