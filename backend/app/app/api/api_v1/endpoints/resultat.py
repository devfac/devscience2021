from typing import Any, List

import sqlalchemy

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.db.session import engine
from sqlalchemy.sql.ddl import CreateSchema
from app.utils import create_anne, decode_schemas, get_credit, get_status, test_semestre
from app.core.config import settings
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from app.resultat import result_by_ue, result_by_session

router = APIRouter()


@router.get("/get_all_notes", response_model=List[Any])
def get_all_notes(
        schemas: str,
        semestre: str,
        session: str,
        uuid_parcours: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_all_note(schemas, semestre, parcours.abreviation, session)
    return all_note


@router.get("/get_by_credit", response_model=List[Any])
def get_by_credit(
        schemas: str,
        semestre: str,
        session: str,
        credit: int,
        uuid_parcours: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_note_by_credit(schemas, semestre, parcours.abreviation, session, credit)
    return all_note


@router.get("/get_by_moyenne", response_model=List[Any])
def get_by_moyenne(
        schemas: str,
        semestre: str,
        session: str,
        moyenne: float,
        uuid_parcours: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_note_by_moyenne(schemas, semestre, parcours.abreviation, session, moyenne)
    return all_note


@router.get("/get_by_moyenne_and_credit_inf", response_model=List[Any])
def get_by_moyenne_and_credit_inf(
        schemas: str,
        semestre: str,
        session: str,
        moyenne: float,
        credit: int,
        uuid_parcours: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_note_by_moyenne_and_credit_inf(schemas, semestre, parcours.abreviation, session, moyenne,
                                                             credit)
    return all_note


@router.get("/get_by_moyenne_and_credit_equals", response_model=List[Any])
def get_by_moyenne_and_credit_equals(
        schemas: str,
        semestre: str,
        session: str,
        credit: int,
        moyenne: float,
        uuid_parcours: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = crud.note.read_note_by_moyenne_and_credit_equals(schemas, semestre, parcours.abreviation, session,
                                                                moyenne, credit)
    return all_note


@router.get("/get_by_moyenne_and_credit_sup", response_model=List[Any])
def get_by_moyenne_and_credit_sup(
        schemas: str,
        semestre: str,
        session: str,
        moyenne: float,
        credit: int,
        uuid_parcours: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")

    all_note = crud.note.read_note_by_moyenne_and_credit_sup(schemas, semestre, parcours.abreviation, session, moyenne,
                                                             credit)
    return all_note


@router.get("/get_by_matier", response_model=schemas.Resultat)
def get_by_matier(
        schemas: str,
        semestre: str,
        session: str,
        value_matier: str,
        uuid_parcours: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    validation = False
    all_columns = crud.note.check_columns_exist(schemas=schemas, semestre=semestre, parcours=parcours.abreviation,
                                                session=session)
    print(all_columns)
    print(value_matier)
    for value in all_columns:
        if value == value_matier:
            validation = True

    if not validation:
        raise HTTPException(status_code=400, detail="matier value not found")
    all_note = {}
    non_valide = crud.note.read_note_failed(schemas, semestre, parcours.abreviation, session, value_matier)
    valide = crud.note.read_note_succes(schemas, semestre, parcours.abreviation, session, value_matier)
    all_note['list_valide'] = valide
    all_note['list_non_valide'] = non_valide
    return all_note


@router.get("/get_by_matier_pdf", response_model=List[Any])
def get_by_matier_pdf(
        schemas: str,
        semestre: str,
        uuid_mention: str,
        uuid_parcours: str,
        session: str,
        value_ue: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    matier_ue = crud.matier_ue.get_by_value(schema=schemas, value=value_ue, semestre=semestre,
                                            uuid_parcours=uuid_parcours)
    if not matier_ue:
        raise HTTPException(status_code=400, detail="value ue not found")
    value_matier = []
    titre_note = []
    value_matier.append(f"ue_{value_ue}")
    titre_note.append("N° Carte")
    titre_note.append(matier_ue.title)
    value_ec = crud.matier_ec.get_by_value_ue(schemas, value_ue, semestre, uuid_parcours)
    for ec in value_ec:
        value_matier.append(f"ec_{ec.value}")
        titre_note.append(ec.title)

    titre_note.append("Crédit")
    titre_note.append("Status")
    matier = ','.join(tuple(value_matier))
    notes = []
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    all_note = crud.note.read_note_by_ue(schemas, semestre, parcours.abreviation.lower(), session, matier)
    etudiant_admis = []
    etudiant_admis_compense = []
    for note in jsonable_encoder(all_note):

        etudiants = {}
        etudiants['N° Carte'] = note["num_carte"]
        etudiants[matier_ue.title] = note[f"ue_{value_ue}"]
        for ec in value_ec:
            etudiants[ec.title] = note[f"ec_{ec.value}"]
        if note[f"ue_{value_ue}"]:
            etudiants['Crédit'] = get_credit(float(note[f"ue_{value_ue}"]), matier_ue.credit)
            etudiants['Status'] = get_status(float(note[f"ue_{value_ue}"]))
            if note[f"ue_{value_ue}"] >= 10:
                info_etudiants = {}
                info_etudiants['N° Carte'] = note["num_carte"]
                un_etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schemas, num_carte=note['num_carte'])
                info_etudiants['nom'] = un_etudiant["nom"]
                info_etudiants['prenom'] = un_etudiant["prenom"]
                etudiant_admis.append(info_etudiants)
        else:
            etudiants['Crédit'] = get_credit(float(0), matier_ue.credit)
            etudiants['Status'] = get_status(float(0))

        if session.lower() == "rattrapage":
            if note[f"ue_{value_ue}"] < 10:
                validation = crud.semetre_valide.get_by_num_carte(schema=schemas, num_carte=note["num_carte"])
                if validation:
                    if test_semestre(validation.semestre, semestre):
                        info_etudiants = {}
                        info_etudiants['N° Carte'] = note["num_carte"]
                        un_etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schemas, num_carte=note['num_carte'])
                        info_etudiants['nom'] = un_etudiant["nom"]
                        info_etudiants['prenom'] = un_etudiant["prenom"]
                        etudiant_admis_compense.append(info_etudiants)
        notes.append(etudiants)
    data = {}
    data['mention'] = mention.title
    data['parcours'] = parcours.title
    data['anne'] = decode_schemas(schemas)
    data['session'] = session
    print(notes)
    file = result_by_ue.PDF.create_result_by_ue(semestre, parcours, data, list(titre_note), notes, etudiant_admis,
                                                etudiant_admis_compense)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/get_by_session_definive", response_model=List[Any])
def get_by_session_definitive_pdf(
        schemas: str,
        semestre: str,
        uuid_mention: str,
        uuid_parcours: str,
        session: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail=f" Parcours not found.", )
    credit = 30
    all_note = crud.note.read_note_by_credit(schemas, semestre, parcours.abreviation.lower(), session, credit)
    etudiant_admis = []
    for note in jsonable_encoder(all_note):
        validation = crud.semetre_valide.get_by_num_carte(schema=schemas, num_carte=note["num_carte"])
        if validation:
            if test_semestre(validation.semestre, semestre):
                info_etudiants = {}
                info_etudiants['N° Carte'] = note["num_carte"]
                un_etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schemas, num_carte=note['num_carte'])
                info_etudiants['nom'] = un_etudiant["nom"]
                info_etudiants['prenom'] = un_etudiant["prenom"]
                etudiant_admis.append(info_etudiants)
    data = {}
    data['mention'] = mention.title
    data['parcours'] = parcours.title
    data['anne'] = decode_schemas(schemas)
    data['session'] = session
    print(etudiant_admis)
    file = result_by_session.PDF.create_result_by_session(semestre, parcours, data, etudiant_admis, "definitive")
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/get_by_session_compense", response_model=List[Any])
def get_by_session_compense_pdf(
        schemas: str,
        semestre: str,
        uuid_mention: str,
        uuid_parcours: str,
        session: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail=f" Parcours not found.", )
    credit = 30
    all_note = crud.note.read_note_by_credit_inf(schemas, semestre, parcours.abreviation.lower(), session, credit)
    etudiant_admis = []
    for note in jsonable_encoder(all_note):
        validation = crud.semetre_valide.get_by_num_carte(schema=schemas, num_carte=note["num_carte"])
        if validation:
            if test_semestre(validation.semestre, semestre):
                info_etudiants = {}
                info_etudiants['N° Carte'] = note["num_carte"]
                un_etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schemas, num_carte=note['num_carte'])
                info_etudiants['nom'] = un_etudiant["nom"]
                info_etudiants['prenom'] = un_etudiant["prenom"]
                etudiant_admis.append(info_etudiants)
    data = {}
    data['mention'] = mention.title
    data['parcours'] = parcours.title
    data['anne'] = decode_schemas(schemas)
    data['session'] = session
    print(etudiant_admis)
    file = result_by_session.PDF.create_result_by_session(semestre, parcours, data, etudiant_admis, "compense")
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)
