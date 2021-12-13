from typing import Any, List

import sqlalchemy

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.db.session import engine
from sqlalchemy.sql.ddl import CreateSchema
from app.utils import create_anne, decode_schemas, get_credit, get_status
from app.core.config import settings
from fastapi.encoders import  jsonable_encoder
from fastapi.responses import FileResponse
from app.resultat import result_by_ue

router = APIRouter()

@router.get("/get_all_notes", response_model=List[Any])
def get_all_notes(
    schemas: str,
    semestre:str,
    session:str,
    uuid_parcours:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_all_note(schemas, semestre, parcours.abreviation,session)
    return all_note


@router.get("/get_by_credit", response_model=List[Any])
def get_by_credit(
    schemas: str,
    semestre:str,
    session:str,
    credit:int,
    uuid_parcours:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_note_by_credit(schemas, semestre, parcours.abreviation,session,credit)
    return all_note

@router.get("/get_by_moyenne", response_model=List[Any])
def get_by_moyenne(
    schemas: str,
    semestre:str,
    session:str,
    moyenne:float,
    uuid_parcours:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_note_by_moyenne(schemas, semestre, parcours.abreviation,session,moyenne)
    return all_note

@router.get("/get_by_moyenne_and_credit_inf", response_model=List[Any])
def get_by_moyenne_and_credit_inf(
    schemas: str,
    semestre:str,
    session:str,
    moyenne:float,
    credit:int,
    uuid_parcours:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_note_by_moyenne_and_credit_inf(schemas, semestre, parcours.abreviation,session,moyenne,credit)
    return all_note


@router.get("/get_by_moyenne_and_credit_equals", response_model=List[Any])
def get_by_moyenne_and_credit_equals(
    schemas: str,
    semestre:str,
    session:str,
    credit:int,
    moyenne:float,
    uuid_parcours:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_note_by_moyenne_and_credit_equals(schemas, semestre, parcours.abreviation,session,moyenne,credit)
    return all_note

@router.get("/get_by_moyenne_and_credit_sup", response_model=List[Any])
def get_by_moyenne_and_credit_sup(
    schemas: str,
    semestre:str,
    session:str,
    moyenne:float,
    credit:int,
    uuid_parcours:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")

    all_note = crud.note.read_note_by_moyenne_and_credit_sup(schemas, semestre, parcours.abreviation,session,moyenne,credit)
    return all_note

@router.get("/get_by_matier", response_model=schemas.Resultat)
def get_by_matier(
    schemas: str,
    semestre:str,
    session:str,
    value_matier:str,
    uuid_parcours:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    validation = False
    all_columns = crud.note.check_columns_exist(schemas=schemas, semestre=semestre,parcours=parcours.abreviation,session=session)
    for value in all_columns:
        if value == value_matier:
            validation = True
    
    if not validation:
        raise HTTPException(status_code=400, detail="matier value not found")
    all_note = {}
    non_valide = crud.note.read_note_failed(schemas, semestre, parcours.abreviation,session,value_matier)
    valide = crud.note.read_note_succes(schemas, semestre, parcours.abreviation,session,value_matier)
    all_note['list_valide'] = valide
    all_note['list_non_valide'] = non_valide
    return all_note

@router.get("/get_by_matier_pdf", response_model=List[Any])
def get_by_matier_pdf(
    schemas: str,
    semestre:str,
    uuid_mention:str,
    uuid_parcours:str,
    session:str,
    value_ue:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    matier_ue = crud.matier_ue.get_by_value(schema=schemas,value=value_ue, semestre=semestre,uuid_parcours=uuid_parcours)
    if not matier_ue:
        raise HTTPException(status_code=400, detail="value ue not found")
    value_matier = []
    titre_note = []
    value_matier.append(f"ue_{value_ue}")
    titre_note.append("N° Carte")
    titre_note.append(matier_ue.title)
    value_ec = crud.matier_ec.get_by_value_ue(schemas,value_ue,semestre,uuid_parcours)
    for ec in value_ec:
        value_matier.append(f"ec_{ec.value}")
        titre_note.append(ec.title)
    
    titre_note.append("Crédit")
    titre_note.append("Status")
    matier = ','.join(tuple(value_matier))
    notes = []
    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    mention = crud.mention.get_by_uuid(db=db,uuid=uuid_mention)
    all_note = crud.note.read_note_by_ue(schemas, semestre, parcours.abreviation.lower(),session,matier)
    for note in jsonable_encoder(all_note):
        etudiants = {}
        etudiants['N° Carte'] = note["num_carte"]
        etudiants[matier_ue.title] = note[f"ue_{value_ue}"]
        for ec in value_ec:
            etudiants[ec.title] = note[f"ec_{ec.value}"]
        etudiants['Crédit'] = get_credit(note[f"ue_{value_ue}"],matier_ue.credit)
        etudiants['Status'] = get_status(note[f"ue_{value_ue}"])
        notes.append(etudiants)
    data ={} 
    data['mention']=mention.title
    data['parcours']=parcours.title
    data['anne']=decode_schemas(schemas)
    data['session']=session
    file = result_by_ue.PDF.create_result_by_ue(semestre,parcours,data,list(titre_note),notes)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)