from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseEnrollmentFee)
def read_enrollment_fee(
        db: Session = Depends(deps.get_db),
        limit: int = 100,
        offset: int = 0,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve enrollment_fees.
    """
    enrollment_fee = crud.enrollment_fee.get_multi(db=db, limit=limit, skip=offset, order_by="level")
    count = crud.enrollment_fee.get_count(db=db)
    response = schemas.ResponseEnrollmentFee(**{'count': count, 'data': enrollment_fee})
    return response


@router.get("/by_mention", response_model=List[schemas.EnrollmentFee])
def read_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        id_mention: str,
        id_year: str,
) -> Any:
    """
    Retrieve enrollment_fees.
    """
    enrollment_fee = crud.enrollment_fee.get_by_mention_and_year(db=db, id_mention=id_mention, id_year=id_year)
    return enrollment_fee


@router.get("/by_id", response_model=schemas.EnrollmentFee)
def read_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        id_enrollment_fee: int,
) -> Any:
    """
    Retrieve enrollment_fees.
    """
    enrollment_fee = crud.enrollment_fee.get(db=db, id=id_enrollment_fee)
    return enrollment_fee


@router.post("/", response_model=schemas.EnrollmentFee)
def create_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        enrollment_fee_in: schemas.EnrollmentFeeCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new enrollment_fee.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    enrollment_fee = crud.enrollment_fee.get_by_level_and_year_mention(
        db=db, level=enrollment_fee_in.level, id_year=enrollment_fee_in.id_year,
        id_mention=enrollment_fee_in.id_mention)
    if enrollment_fee:
        raise HTTPException(status_code=400, detail="enrollment_fee already exist")

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_in)
    return enrollment_fee


@router.put("/", response_model=schemas.EnrollmentFee)
def update_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        id_enrollment_fee: int,
        enrollment_fee_in: schemas.EnrollmentFeeUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an enrollment_fee.
    """
    enrollment_fee = crud.enrollment_fee.get(db=db, id=id_enrollment_fee)
    if not enrollment_fee:
        raise HTTPException(status_code=404, detail="enrollment_fee not found")
    enrollment_fee = crud.enrollment_fee.update(db=db, db_obj=enrollment_fee, obj_in=enrollment_fee_in)
    return enrollment_fee


@router.get("/by_level_and_year", response_model=schemas.EnrollmentFee)
def read_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        id_mention: str,
        id_year: int,
        level: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get enrollment_fee by ID.
    """
    enrollment_fee = crud.enrollment_fee.get_by_level_and_year_mention(
        db=db, level=level, id_year=id_year, id_mention=id_mention)
    if not enrollment_fee:
        raise HTTPException(status_code=404, detail="enrollment_fee not found")
    return enrollment_fee


@router.delete("/", response_model=Any)
def delete_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        id_enrollment_fee: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an enrollment_fee.
    """
    enrollment_fee = crud.enrollment_fee.get(db=db, id=id_enrollment_fee)
    if not enrollment_fee:
        raise HTTPException(status_code=404, detail="enrollment_fee not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    enrollment_fee = crud.enrollment_fee.remove(db=db, id=id_enrollment_fee)
    return enrollment_fee
