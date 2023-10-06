from datetime import datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import format_date

router = APIRouter()


@router.get("/", response_model=List[schemas.Permission])
def read_permissions(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve permissions.
    """
    if crud.user.is_superuser(current_user):
        permission = crud.permission.get_multi(db=db)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return permission


@router.post("/", response_model=schemas.Permission)
def create_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission_in: schemas.PermissionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new permission.
    """
    user = crud.user.get_by_email(db=db, email=permission_in.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    expiration_date = datetime.now() + timedelta(hours=permission_in.time)
    permission_model = schemas.PermissionCreateModel(**{'email': permission_in.email,
                                                        'expiration_date': expiration_date.astimezone(),
                                                        'accepted': permission_in.accepted,
                                                        'type': permission_in.type,
                                                        'updated_at': datetime.now().astimezone()
                                                        })
    permission = crud.permission.get_by_email_and_type(db=db, email=permission_model.email, type_=permission_in.type)
    if not permission:
        permission = crud.permission.create(db=db, obj_in=permission_model, email_sender=current_user.email)
    else:
        permissionUpdate = schemas.PermissionUpdate(**{'email': permission_in.email,
                                                       'expiration_date': expiration_date.astimezone(),
                                                       'accepted': permission_in.accepted,
                                                       'type': permission_in.type,
                                                       'updated_at': datetime.now().astimezone(),
                                                       'email_sender': current_user.email
                                                       })
        permission = crud.permission.update(db=db, obj_in=permissionUpdate, db_obj=permission)
    return permission


@router.get("/get_by_email_and_type/", response_model=schemas.Permission)
def get_by_email_and_type(
        *,
        db: Session = Depends(deps.get_db),
        email: str,
        type_: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get permission by ID.
    """
    permission = crud.permission.get_by_email_and_type(db=db, email=email, type_=type_)
    if permission:
        if format_date() >= format_date(date_=permission.expiration_date):
            permission_obj = schemas.PermissionUpdate(**{'accepted': False})
            permission = crud.permission.update(db=db, obj_in=permission_obj, db_obj=permission)
        return permission
    return schemas.Permission(**{'accepted': False})


@router.delete("/", response_model=schemas.Permission)
def delete_permission(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an permission.
    """
    permission = crud.permission.get_by_id(db=db, uuid=uuid)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    if permission.email != current_user.email or not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    permission = crud.permission.remove_id(db=db, uuid=uuid)
    return permission
