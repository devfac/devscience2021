from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseUserMention)
def read_user_mentions(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user_mentions.
    """
    user_mention = crud.user_mention.get_multi(db=db, skip=offset, limit=limit)
    count = crud.user_mention.get_count(db=db)
    response = schemas.ResponseUserMention(**{'count': count, 'data': user_mention})
    return response


@router.post("/", response_model=List[schemas.UserMention])
def create_user_mention(
        *,
        db: Session = Depends(deps.get_db),
        user_mention_in: schemas.UserMentionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user_mention.
    """
    if crud.user.is_superuser(current_user):
        user_mention = crud.user_mention.create(db=db, obj_in=user_mention_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.user_mention.get_multi(db=db)


@router.put("/", response_model=List[schemas.UserMention])
def update_user_mention(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        user_mention_in: schemas.UserMentionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an user_mention.
    """
    user_mention = crud.user_mention.get_by_id(db=db, uuid=uuid)
    if not user_mention:
        raise HTTPException(status_code=404, detail="UserMention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    user_mention = crud.user_mention.update(db=db, db_obj=user_mention, obj_in=user_mention_in)
    return crud.user_mention.get_multi(db=db)


@router.get("/by_id/", response_model=schemas.UserMention)
def read_user_mention(
        *,
        db: Session = Depends(deps.get_db),
        user_mention_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user_mention by ID.
    """
    user_mention = crud.user_mention.get_by_id(db=db, user_mention_id=user_mention_id)
    if not user_mention:
        raise HTTPException(status_code=404, detail="UserMention not found")
    return user_mention


@router.get("/by_user/", response_model=List[schemas.UserMention])
def read_user_mention(
        *,
        db: Session = Depends(deps.get_db),
        id_user: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user_mention by ID.
    """
    user_mention = crud.user_mention.get_by_user(db=db, id_user=id_user)
    return user_mention

@router.delete("/", response_model=List[schemas.UserMention])
def delete_user_mention(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an user_mention.
    """
    user_mention = crud.user_mention.get_by_id(db=db, uuid=uuid)
    if not user_mention:
        raise HTTPException(status_code=404, detail="UserMention not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    user_mention = crud.user_mention.remove_id(db=db, uuid=uuid)
    return crud.user_mention.get_multi(db=db)
