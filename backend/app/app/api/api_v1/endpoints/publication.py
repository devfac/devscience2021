import os
from os import getcwd
from typing import List
from typing import Optional

from fastapi import APIRouter, UploadFile, File
from fastapi import Depends, Response
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from app import models
from app.api import deps
from app.crud import publication
from app.schemas.publication import PublicationCreate, PublicationUpdate
from app.schemas.publication import ShowPublication
from app.schemas.response import ResponseData

router = APIRouter()


@router.post("/", response_model=ShowPublication, response_model_exclude_none=True)
async def create_publication(
        publications: PublicationCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
):
    publications = publication.create_publications(obj_in=publications, db=db)
    return publications


@router.get(
    "/", response_model=ShowPublication
)  # if we keep just "{uuid}" . it would stat catching all routes
def read_publication(uuid: str, db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)):
    publications = publication.retreive_publication(uuid=uuid, db=db)
    if not publications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Publication with this uuid {uuid} does not exist",
        )
    return publications


@router.get("/admin", response_model=ResponseData)
def read_publications(
        db: Session = Depends(deps.get_db),
        limit: int = 100,
        offset: int = 0,
        order: str = "desc",
        order_by: str = "title",
        current_user: models.User = Depends(deps.get_current_active_user),
):
    count = len(publication.get_count(db=db))
    publications = publication.list_publications_admin(db=db, limit=limit, skip=offset)

    response = ResponseData(**{'count': count, 'data': publications})
    return response


@router.get("/", response_model=List[ShowPublication])
def read_publications(
        response: Response,
        db: Session = Depends(deps.get_db), ):
    publications = publication.list_publications(db=db)

    response.headers["Content-Range"] = f"0-9/{len(publications)}"
    return publications


@router.put("/", response_model=ShowPublication)
def update_publication(
        uuid: str, obj_in: PublicationUpdate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
                       ):
    publications = publication.retreive_publication(uuid=uuid, db=db)
    if not publications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Publication with uuid {uuid} not found"
        )
    publications = publication.update(db=db, db_obj=publications, obj_in=obj_in)
    return publications


@router.delete("/")
def delete_publication(
        uuid: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
):
    publications = publication.retreive_publication(uuid=uuid, db=db)
    if not publications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Publication with uuid {uuid} not found"
        )
    publications = publication.remove(db=db, id=uuid)
    return publications


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(deps.get_db)):
    publications = publication.search_publication(term, db=db)
    publication_titles = []
    for item_publication in publications:
        publication_titles.append(item_publication.title)
    return publication_titles