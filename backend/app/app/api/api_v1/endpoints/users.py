from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_all/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db=db)
    return users


@router.post("/", response_model=List[schemas.User])
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
    #if check_email_valide(user_in.email) == "valid": 
    #    send_new_account(user_in.email,user_in.password)
    #    user = crud.user.create(db, obj_in=user_in)
    #else:
    #    raise HTTPException(
    #        status_code=400,
    #        detail="email not valid.",
    #    )
    user = crud.user.create(db, obj_in=user_in)
    return crud.user.get_multi(db=db)


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

#
# @router.post("/open", response_model=schemas.User)
# def create_user_open(
#     *,
#     db: Session = Depends(deps.get_db),
#     password: str = Body(...),
#     email: EmailStr = Body(...),
#     full_name: str = Body(None),
# ) -> Any:
#     """
#     Create new user not need to be logged in.
#     """
#     if not settings.USERS_OPEN_REGISTRATION:
#         raise HTTPException(
#             status_code=403,
#             detail="Open user registration is forbidden on this server",
#         )
#     user = crud.user.get_by_email(db, email=email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system",
#         )
#     user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
#     user = crud.user.create(db, obj_in=user_in)
#     return user


@router.get("/", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/", response_model=List[schemas.User])
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get_by_uuid(db, uuid=uuid)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return crud.user.get_multi(db=db)


@router.delete("/", response_model=List[schemas.User])
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an user.
    """
    user = crud.user.get_by_uuid(db=db, uuid=uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    user = crud.user.remove_uuid(db=db, uuid=uuid)
    return crud.user.get_multi(db=db)

