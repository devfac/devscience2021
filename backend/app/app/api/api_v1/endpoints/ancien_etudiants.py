import datetime
import json
import os
import uuid
from os import getcwd
from typing import Any, List
from uuid import UUID

from app import crud, models, schemas
from app.api import deps
from app.utils import UUIDEncoder
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.script_logging import ScriptLogging

router = APIRouter()


@router.get("/", response_model=List[schemas.EtudiantAncien])
def read_etudiant_ancienne(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve etudiant ancienne.
    """

    logging_ = ScriptLogging(current_user.email)
    etudiant = crud.ancien_etudiant.get_all(schema=schema)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            parcours = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours)
            print(un_etudiant.uuid_parcours)
            if parcours:
                et["parcours"] = parcours.abbreviation
            list_et.append(et)

    logging_.script_logging("error",
                            f"GET:======={datetime.datetime.now()}=======Ancien etudiant========"
                            f"Anne Univ not found")
    return list_et


@router.post("/", response_model=List[schemas.EtudiantAncien])
def create_etudiant_ancien(
        *,
        db: Session = Depends(deps.get_db),
        etudiant_in: schemas.EtudiantAncienCreate,
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new etudiant.
    """

    logging_ = ScriptLogging(current_user.email)
    etudiant_in.uuid = uuid.uuid4()
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=etudiant_in.num_carte)
    if etudiant:
        logging_.script_logging("error",
                                f"POST:======={datetime.datetime.now()}======={dict(etudiant_in)}========"
                                f"Etudiant already exists")
        raise HTTPException(status_code=404, detail="Etudiant already exists")
    etudiant = crud.ancien_etudiant.create_etudiant(schema=schema, obj_in=etudiant_in)
    list_et = []
    if etudiant:
        logging_.script_logging("info",
                                f"POST:======={datetime.datetime.now()}======={dict(etudiant_in)}========"
                                f"Success")
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.put("/update_etudiant/", response_model=List[schemas.EtudiantAncien])
def update_etudiant(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        schema: str,
        etudiant_in: schemas.EtudiantAncienUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an etudiant.
    """

    logging_ = ScriptLogging(current_user.email)
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not etudiant:
        logging_.script_logging("error",
                                f"PUT:======={datetime.datetime.now()}======={dict(etudiant_in)}========"
                                f"Etudiant not found")
        raise HTTPException(status_code=404, detail="Etudiant not found")
    etudiant = crud.ancien_etudiant.update_etudiant(schema=schema, num_carte=num_carte, obj_in=etudiant_in)
    list_et = []
    if etudiant:
        logging_.script_logging("info",
                                f"PUT:======={datetime.datetime.now()}======={dict(etudiant_in)}========"
                                f"Success")
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.get("/by_num/", response_model=schemas.EtudiantAncien)
def read_etudiant_by_num_carte(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by num carte.
    """
    logging_ = ScriptLogging(current_user.email)
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not etudiant:
        logging_.script_logging("error",
                                f"GET:======={datetime.datetime.now()}=======Ancien etudiant========"
                                f"Etudiant not found")
        raise HTTPException(status_code=404, detail="Etudiant not found")

    logging_.script_logging("info",
                            f"GET:======={datetime.datetime.now()}=======Ancien etudiant========"
                            f"Success")
    et = json.loads(json.dumps(dict(etudiant), cls=UUIDEncoder))
    et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=etudiant.uuid_parcours).abbreviation
    return et


@router.get("/by_mention/", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_mention(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid_mention: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by mention.
    """
    logging_ = ScriptLogging(current_user.email)
    etudiant = crud.ancien_etudiant.get_by_mention(schema=schema, uuid_mention=uuid_mention)
    list_et = []
    if etudiant:
        logging_.script_logging("info",
                                f"GET:======={datetime.datetime.now()}=======Ancien etudiant========"
                                f"Success")
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.get("/by_parcours/", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_parcours(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid_parcours: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by parcours.
    """
    logging_ = ScriptLogging(current_user.email)
    etudiant = crud.ancien_etudiant.get_by_parcours(schema=schema, uuid_parcours=uuid_parcours)
    list_et = []
    if etudiant:
        logging_.script_logging("info",
                                f"GET:======={datetime.datetime.now()}=======Ancien etudiant========"
                                f"Success")
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.get("/by_semetre_and_mention/", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_semstre_and_mention(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid_mention: UUID,
        semetre_grand: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by semestre and mention.
    """
    etudiant = crud.ancien_etudiant.get_by_semetre_and_mention(
        schema=schema, uuid_mention=uuid_mention, semetre_grand=semetre_grand)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.get("/by_etat/", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_etat(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        etat: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by etat.
    """
    etudiant = crud.ancien_etudiant.get_by_etat(schema=schema, etat=etat)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.get("/by_etat_and_moyenne/", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_etat_and_moyenne(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        etat: str,
        moyenne: float,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by etat and moyenne.
    """
    etudiant = crud.ancien_etudiant.get_by_etat_and_moyenne(schema=schema, etat=etat, moyenne=moyenne)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.get("/by_class/", response_model=List[schemas.EtudiantAncien])
def read_etudiant_by_class(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid_parcours: str,
        semestre: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by class.
    """
    etudiant = crud.ancien_etudiant.get_by_class(schema, uuid_parcours, semestre)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.delete("/", response_model=List[schemas.EtudiantAncien])
def delete_etudiant(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an etudiant.
    """
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    etudiant = crud.ancien_etudiant.delete_etudiant(schema=schema, num_carte=num_carte)
    list_et = []
    if etudiant:
        for un_etudiant in etudiant:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abbreviation
            list_et.append(et)
    return list_et


@router.get("/photo")
def get_file(name_file: str):
    return FileResponse(path=getcwd() + "/files/photos/" + name_file)


@router.post("/upload_photo/")
async def create_upload_file(*,
                             uploaded_file: UploadFile = File(...),
                             num_carte: str,
                             current_user: models.User = Depends(deps.get_current_active_user)
                             ):

    name = list(os.path.splitext(uploaded_file.filename))[1]
    allowed_files = {".jpg", ".jpeg", ".png"}

    if name.lower() not in allowed_files:
        raise HTTPException(status_code=402, detail="invalid image")
    file_location = f"files/photos/{num_carte}{name}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"filename": f'{num_carte}{name}'}
