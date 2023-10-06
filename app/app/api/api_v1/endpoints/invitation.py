from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Invitation])
def read_invitations(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve invitations.
    """
    if crud.user.is_superuser(current_user):
        invitation = crud.invitation.get_multi(db=db)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return invitation


@router.post("/", response_model=schemas.Invitation)
def create_invitation(
    *,
    db: Session = Depends(deps.get_db),
    invitation_in: schemas.InvitationCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new invitation.
    """
    if crud.user.is_superuser(current_user):
        invitation = crud.invitation.create(db=db, obj_in=invitation_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return invitation


@router.put("/", response_model=schemas.Invitation)
def update_invitation(
    *,
    db: Session = Depends(deps.get_db),
    id_invitation: int,
    invitation_in: schemas.InvitationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an invitation.
    """
    invitation = crud.invitation.get(db=db, id=id_invitation)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    invitation = crud.invitation.update(db=db, db_obj=invitation, obj_in=invitation_in)
    return invitation


@router.get("/by_id/", response_model=schemas.Invitation)
def read_invitation(
    *,
    db: Session = Depends(deps.get_db),
    id_invitation: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get invitation by ID.
    """
    invitation = crud.invitation.get(db=db, id=id_invitation)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return invitation


@router.delete("/", response_model=schemas.Invitation)
def delete_invitation(
    *,
    db: Session = Depends(deps.get_db),
    id_invitation: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an invitation.
    """
    invitation = crud.invitation.get(db=db, id=id_invitation)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    if invitation.email != current_user.email:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    invitation = crud.invitation.remove(db=db, id=id_invitation)
    return invitation
