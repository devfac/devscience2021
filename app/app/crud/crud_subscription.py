from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):

    def get_by_id(self, db: Session, *, subscription_id: str) -> Optional[Subscription]:
        return db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    def get_num_carte(self, db: Session, *, num_carte: str) -> Optional[Subscription]:
        return db.query(Subscription).filter(Subscription.num_carte == num_carte).first()


subscription = CRUDSubscription(Subscription)
