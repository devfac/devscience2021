from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
import json
router = APIRouter()


@router.get("/", response_model=schemas.ResponseData)
def read_historic(
    db: Session = Depends(deps.get_db),
    *,
    college_year: str = "",
    email: str = "",
    offset: int = 0,
    title:str = "",
    limit: int = 100,
    order: str = "DESC",
    order_by: str = "created_at",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve historics.
    """
    if crud.user.is_superuser(current_user):
        historic = crud.historic.get_all(db=db, limit=limit, skip=offset, college_year=college_year,
                                         email=email, order_by=order_by, order=order, title=title)
        count = len(crud.historic.get_count(db=db, college_year=college_year, email=email, title=title))
        response = schemas.ResponseData(**{'count':count, 'data':historic})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.get("/me/", response_model=schemas.ResponseData)
def read_my_historic(
    *,
    db: Session = Depends(deps.get_db),
    college_year: str = "",
    title:str = "",
    offset: int = 0,
    limit: int = 100,
    order: str = "DESC",
    order_by: str = "created_at",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get historic by ID.
    """
    all_history = []
    histories = crud.historic.get_by_email(db=db, college_year=college_year, skip=offset,
                                          limit=limit, order_by=order_by, order=order,
                                           email=current_user.email, title=title)
    for historic in histories:
        if historic.action != "":
            action = json.loads(historic.action.replace("'",'"'))
        else:
            action = []
        historic.action = action
        all_history.append(historic)
    count = len(crud.historic.get_count(db=db, college_year=college_year, email=current_user.email, title=title))
    response = schemas.ResponseData(**{'count': count, 'data': all_history})
    return response


@router.delete("/", response_model=List[schemas.Historic])
def delete_historic(
    *,
    db: Session = Depends(deps.get_db),
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an historic.
    """
    historic = crud.historic.get_by_uuid(db=db, uuid=uuid)
    if not historic:
        raise HTTPException(status_code=404, detail="Historic not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    historic = crud.historic.remove_uuid(db=db, uuid=uuid)
    return crud.historic.get_multi(db=db, order_by="created_at")
