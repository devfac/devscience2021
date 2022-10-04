from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import decode_text

router = APIRouter()


@router.get("/", response_model=List[schemas.Mention])
def read_mentions(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve mentions.
    """
    mentions = crud.mention.get_multi(db=db)
    return mentions


@router.post("/", response_model=List[schemas.Mention])
def create_mention(
    *,
    db: Session = Depends(deps.get_db),
    mention_in: schemas.MentionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new mention.
    """
    value = decode_text(mention_in.title).lower()
    mention = crud.mention.get_by_value(db=db, value=value)
    if mention:
        raise HTTPException(status_code=400, detail="Mention already exist")

    if crud.user.is_superuser(current_user):
        mention = crud.mention.create(db=db, obj_in=mention_in, value=value)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.mention.get_multi(db=db)


@router.put("/", response_model=List[schemas.Mention])
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
    mention_oj = {}
    if mention_in.title:
        mention_oj['title']=mention_in.title
        mention_oj['value']=decode_text(mention_in.title).lower()
    if mention_in.last_num_carte:
        mention_oj['last_num_carte']=mention_in.last_num_carte
    if mention_in.plugged:
        mention_oj['plugged']=decode_text(mention_in.plugged)
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    mention = crud.mention.update(db=db, db_obj=mention, obj_in=mention_oj)
    return crud.mention.get_multi(db=db)


@router.get("/{uuid}", response_model=schemas.Mention)
def read_mention(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get mention by ID.
    """
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")
    return mention


@router.delete("/", response_model=List[schemas.Mention])
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
    return crud.mention.get_multi(db=db)
