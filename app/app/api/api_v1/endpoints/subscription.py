from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ResponseSubscription)
def read_subscriptions(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve subscriptions.
    """
    if crud.user.is_superuser(current_user):
        subscription = crud.subscription.get_multi(db=db, order_by="num_carte")
        count = len(crud.subscription.get_count(db=db))
        response = schemas.ResponseSubscription(**{'count': count, 'data': subscription})
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return response


@router.post("/", response_model=schemas.Subscription)
def create_subscription(
        *,
        db: Session = Depends(deps.get_db),
        subscription_in: schemas.SubscriptionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new subscription.
    """
    subscription = crud.subscription.create(db=db, obj_in=subscription_in)
    return subscription


@router.put("/", response_model=schemas.Subscription)
def update_subscription(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        subscription_in: schemas.SubscriptionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an subscription.
    """
    subscription = crud.subscription.get_by_id(db=db, uuid=uuid)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription = crud.subscription.update(db=db, db_obj=subscription, obj_in=subscription_in)
    return subscription


@router.get("/by_id/", response_model=schemas.Subscription)
def read_subscription(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get subscription by ID.
    """
    subscription = crud.subscription.get_by_id(db=db, uuid=uuid)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.delete("/", response_model=schemas.Subscription)
def delete_subscription(
        *,
        db: Session = Depends(deps.get_db),
        uuid: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an subscription.
    """
    subscription = crud.subscription.get_by_id(db=db, uuid=uuid)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription = crud.subscription.remove_id(db=db, uuid=uuid)
    return subscription
