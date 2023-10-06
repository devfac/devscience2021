import ast
from typing import Any, List
from uuid import UUID
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=Any)
def create_interaction(
        *,
        db: Session = Depends(deps.get_db),
        interaction_in: schemas.InteractionCreate,
        semester: str,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new interaction.
    """
    if crud.user.is_superuser(current_user):
        interaction = crud.interaction.get_by_journey_and_year(
            db=db, id_journey=interaction_in.id_journey,
            id_year=interaction_in.id_year)
        interaction_value = jsonable_encoder(interaction_in)
        if not interaction:
            list_value = []
            for value in interaction_value[semester.lower()]:
                list_value.append(str(dict(value)))
            interaction_value[semester.lower()] = list_value
            for i in range(10):
                if f"s{(i+1)}" != semester.lower():
                    interaction_value[f"s{(i+1)}"] = None
            interaction = crud.interaction.create(db=db, obj_in=interaction_value)
        else:
            list_value = []
            new_value = {}
            for value in interaction_value[semester.lower()]:
                list_value.append(str(dict(value)))
            interaction_value[semester.lower()] = list_value

            for data in interaction_value:
                if interaction_value[data]:
                    new_value[data] = interaction_value[data]

            interaction = crud.interaction.update(db=db, db_obj=interaction, obj_in=new_value)

        interaction_value = jsonable_encoder(interaction)
        list_value = []
        for value in interaction_value[semester.lower()]:
            value = ast.literal_eval(value)
            list_value.append(value)
        interaction = jsonable_encoder(interaction)
        interaction[semester.lower()] = list_value
        return interaction[semester.lower()]
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.get("/", response_model=List[schemas.ValueUEEC])
def get_by_journey_year(
        *,
        db: Session = Depends(deps.get_db),
        semester: str,
        id_journey: UUID,
        id_year: str,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an interaction.
    """

    interaction = crud.interaction.get_by_journey_and_year(
        db=db, id_journey=id_journey,
        id_year=id_year)
    if not interaction:
        raise HTTPException(status_code=404, detail="interaction not found")
    interaction_value = jsonable_encoder(interaction)
    list_value = []
    for value in interaction_value[semester.lower()]:
        value = ast.literal_eval(value)
        list_value.append(value)
    interaction = jsonable_encoder(interaction)
    interaction[semester.lower()] = list_value
    return interaction[semester.lower()]


@router.delete("/{uuid}", response_model=List[schemas.Interaction])
def delete_interaction(
        *,
        db: Session = Depends(deps.get_db),
        id_journey: UUID,
        id_year: int,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an interaction.
    """
    interaction = crud.interaction.get_by_journey_and_year(
        db=db, id_journey=id_journey,
        id_year=id_year)
    if not interaction:
        raise HTTPException(status_code=404, detail="interaction not found")

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    interaction = crud.interaction.remove_id(db=db, uuid=interaction.id)
    return interaction
