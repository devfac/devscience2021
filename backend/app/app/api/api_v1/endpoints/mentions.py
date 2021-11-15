from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Mention])
def read_mentions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve mentions.
    """
    if crud.user.is_superuser(current_user):
        mentions = crud.mention.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return mentions


@router.post("/", response_model=schemas.Mention)
def create_mention(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.MentionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new mention.
    """
    if crud.user.is_superuser(current_user):
        mention = crud.mention.create(db=db, obj_in=item_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return mention


@router.put("/{id}", response_model=schemas.Mention)
def update_mention(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    mention_in: schemas.MentionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an mention.
    """
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    mention = crud.mention.update(db=db, db_obj=mention, obj_in=mention_in)
    return mention


@router.get("/{uuid}", response_model=schemas.Mention)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get mention by ID.
    """
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return mention


@router.delete("/{uuid}", response_model=schemas.Mention)
def delete_mention(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an mention.
    """
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    mention = crud.mention.remove_uuid(db=db, uuid=uuid)
    return mention
