import datetime
import uuid

from sqlalchemy import text

from app.models.publication import Publication
from app.schemas.publication import PublicationCreate, PublicationUpdate
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase


class CRUDPublications(CRUDBase[Publication, PublicationCreate, PublicationUpdate]):
    def create_publications(self, obj_in: PublicationCreate, db: Session):
        publication_object = Publication(**obj_in.dict(), uuid=str(uuid.uuid4()),
                                         created_at=datetime.datetime.now().astimezone())
        db.add(publication_object)
        db.commit()
        db.refresh(publication_object)
        return publication_object

    def retreive_publication(self, uuid: str, db: Session):
        item = db.query(Publication).filter(Publication.uuid == uuid).first()
        return item

    def list_publications(self, db: Session):  # new
        publications = db.query(Publication).filter(Publication.expiration_date >= datetime.date.today()).all()
        return publications

    def list_publications_admin(self, db: Session, limit: int = 100, skip: int = 0,
                                order_by: str = "title", order: str = "ASC",):  # new
        return (
            db.query(Publication)
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all())

    def delete_publication_by_id(self, uuid: str, db: Session, owner_id):
        existing_publication = db.query(Publication).filter(Publication.uuid == uuid)
        if not existing_publication.first():
            return 0
        existing_publication.delete(synchronize_session=False)
        db.commit()
        return 1

    def search_publication(self, query: str, db: Session):
        publications = db.query(Publication).filter(Publication.title.contains(query))
        return publications


publication = CRUDPublications(Publication)
