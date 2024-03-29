from datetime import timedelta, datetime
from typing import Any
import logging
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.script_logging import ScriptLogging
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()

@router.post("/login/access-token", response_model=schemas.UserLogin)
def login_access_token(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    logger = ScriptLogging(user.email)
    logger.script_logging("info",user.email, f"connected at {datetime.now()}")
    if user.is_superuser:
        permission = "super_admin"
    else:
        permission = "user"

    role = crud.role.get_by_uuid(db, uuid=user.uuid_role)
    if role:
        role_value = role.title
    else:
        role_value = "admin"
    list_mention = []
    if user.uuid_mention:
        for uuid in user.uuid_mention:
            mention = crud.mention.get_by_uuid(db=db, uuid=uuid)
            if mention:
                list_mention.append(mention.title)
    token = security.create_access_token(
        data={"uuid": str(user.uuid), "email": form_data.username, "permissions": permission, "role": role_value,
              "mention": user.uuid_mention},
        expires_delta=access_token_expires
    )
    token_data = deps.get_user(token)
    user = crud.user.get(db=db, uuid=token_data.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = schemas.UserLogin(**jsonable_encoder(user), access_token=token, role=role_value, mention=list_mention)
    historic = schemas.HistoricCreate(email=user.email,
                                      value=f"login_system",
                                      title=f"Login System",
                                      action="",
                                      college_year="")
    crud.historic.create(db=db, obj_in=historic)
    return user


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/login/test-token/{token}", response_model=schemas.User)
def test_token(token: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Test access token
    """
    token_data = deps.get_user(token)
    user = crud.user.get(db=db, uuid=token_data.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/decode_token", response_model=schemas.TokenPayload)
def test_token(token_info=Depends(deps.get_token_info)) -> Any:
    """
    Test access token
    """
    return token_info


@router.post("/password-recovery/", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
