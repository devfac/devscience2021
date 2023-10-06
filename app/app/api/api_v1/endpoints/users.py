from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import send_student_transcript

router = APIRouter()


@router.get("/send_email/", response_model=Any)
def read_users(
        *,
        email: str,
        semester: str,
        name: str,
        num_carte: str,
) -> Any:
    send_student_transcript(email_to=email, semester=semester, name=name, num_carte=num_carte)


@router.get("/get_all/", response_model=schemas.ResponseUser)
def read_users(
        db: Session = Depends(deps.get_db),
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(100, description="Limit for pagination"),
        wheres: List[Any] = Query([], description="Filter conditions"),
        order: str = "ASC",
        order_by: str = "last_name",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db=db, limit=limit, skip=offset, order_by=order_by, order=order, where=wheres)
    all_users = []
    count = crud.user.get_count(db=db)
    for on_user in users:
        on_user.list_mention = crud.user_mention.get_by_user(db=db, id_user=on_user.id)
        all_users.append(on_user)
    response = schemas.ResponseUser(**{'count': count, 'data': all_users})
    return response


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = crud.user.create(db, obj_in=user_in)
    if user:
        if user_in.id_mention:
            for id_mention in user_in.id_mention:
                user_mention_in = schemas.UserMentionCreate(
                    id_mention=id_mention, id_user=user.id
                )
                crud.user_mention.create(db=db, obj_in=user_mention_in)
    return user


@router.put("/me/", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        new_password: str,
        old_password: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    user = crud.user.authenticate(
        db, email=user_in.email, password=old_password
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect password",
        )

    if new_password is not None:
        user_in.password = new_password
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    user.list_mention = crud.user_mention.get_by_user(db=db, id_user=user.id)
    return user


@router.get("/me", response_model=Any)
def read_user_me(
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/by_id/", response_model=schemas.User)
def read_user_by_id(
        user_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db=db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user.list_mention = crud.user_mention.get_by_user(db=db, id_user=user.id)
    return user


@router.put("/", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: str,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    list_mention = crud.user_mention.get_by_user(db=db, id_user=user.id)
    for id_user_mention in list_mention:
        crud.user_mention.remove(db=db, id=id_user_mention.id)
    if user:
        if user_in.id_mention:
            for mention in user_in.id_mention:
                user_mention_in = schemas.UserMentionCreate(
                    id_mention=mention, id_user=user.id
                )
                crud.user_mention.create(db=db, obj_in=user_mention_in)
    user.list_mention = crud.user_mention.get_by_user(db=db, id_user=user.id)
    return user


@router.delete("/", response_model=Any)
def delete_user(
        *,
        db: Session = Depends(deps.get_db),
        id_user: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an user.
    """
    user = crud.user.get(db=db, id=id_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    list_mention = crud.user_mention.get_by_user(db=db, id_user=user.id)
    all_historic = crud.historic.get_by_user(db=db, email=user.email)
    all_permission = crud.permission.get_by_email(db=db, email=user.email)
    for permission in all_permission:
        crud.permission.remove(db=db, id=permission.id)
    for historic in all_historic:
        crud.historic.remove(db=db, id=historic.id)
    for mention_user in list_mention:
        crud.user_mention.remove(db=db, id=mention_user.id)
    crud.user.remove(db=db, id=id_user)
    return user
