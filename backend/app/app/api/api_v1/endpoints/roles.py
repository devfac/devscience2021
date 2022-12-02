from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_roles(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve roles.
    """
    if crud.user.is_superuser(current_user):
        role = crud.role.get_multi(db=db)
        count = len(crud.role.get_count(db=db))
        response = schemas.ResponseData(**{'count':count, 'data':role})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=List[schemas.Role])
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: schemas.RoleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new role.
    """
    if crud.user.is_superuser(current_user):
        role = crud.role.create(db=db, obj_in=role_in)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.role.get_multi(db=db)


@router.put("/", response_model=List[schemas.Role])
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    role_in: schemas.RoleUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an role.
    """
    role = crud.role.get_by_uuid(db=db, uuid=uuid)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    role = crud.role.update(db=db, db_obj=role, obj_in=role_in)
    return crud.role.get_multi(db=db)


@router.get("/by_uuid/", response_model=schemas.Role)
def read_role(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get role by ID.
    """
    role = crud.role.get_by_uuid(db=db, uuid=uuid)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return role


@router.delete("/", response_model=List[schemas.Role])
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an role.
    """
    role = crud.role.get_by_uuid(db=db, uuid=uuid)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    role = crud.role.remove_uuid(db=db, uuid=uuid)
    return crud.role.get_multi(db=db)
