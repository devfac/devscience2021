from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.drive_script import create_forlder_and_spreadsheet, write_data_to_drive

router = APIRouter()


@router.post("/create_spreadsheet", response_model=schemas.Msg, )
def create_spreadsheet(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create forlder and worksheet
    """
    print("begin")
    response = create_forlder_and_spreadsheet(db)
    return {"msg": f"{response}"}


@router.post("/write_data", response_model=schemas.Msg)
def write_data(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    write data to worksheet
    """
    response = write_data_to_drive(db)
    return {"msg": f"{response}"}
