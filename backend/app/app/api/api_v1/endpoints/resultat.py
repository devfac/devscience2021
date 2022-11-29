from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.resultat import result_by_ue, result_by_session
from app.utils import decode_schemas, get_credit, get_status, test_semester
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/get_all_notes", response_model=List[Any])
def get_all_notes(
        semester: str,
        session: str,
        uuid_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    all_note = crud.note.read_all_note(create_anne(schemas), semester, journey.abbreviation, session)
    return all_note


@router.get("/get_by_credit", response_model=List[Any])
def get_by_credit(
        schemas: str,
        semester: str,
        session: str,
        credit: int,
        uuid_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    all_note = crud.note.read_note_by_credit(schemas, semester, journey.abbreviation, session, credit)
    return all_note


@router.get("/get_by_moyenne", response_model=List[Any])
def get_by_moyenne(
        schemas: str,
        semester: str,
        session: str,
        moyenne: float,
        uuid_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    all_note = crud.note.read_note_by_moyenne(schemas, semester, journey.abbreviation, session, moyenne)
    return all_note


@router.get("/get_by_moyenne_and_credit_inf", response_model=List[Any])
def get_by_moyenne_and_credit_inf(
        schemas: str,
        semester: str,
        session: str,
        moyenne: float,
        credit: int,
        uuid_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    all_note = crud.note.read_note_by_moyenne_and_credit_inf(schemas, semester, journey.abbreviation, session, moyenne,
                                                             credit)
    return all_note


@router.get("/get_by_moyenne_and_credit_equals", response_model=List[Any])
def get_by_moyenne_and_credit_equals(
        schemas: str,
        semester: str,
        session: str,
        credit: int,
        moyenne: float,
        uuid_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    all_note = crud.note.read_note_by_moyenne_and_credit_equals(schemas, semester, journey.abbreviation, session,
                                                                moyenne, credit)
    return all_note


@router.get("/get_by_moyenne_and_credit_sup", response_model=List[Any])
def get_by_moyenne_and_credit_sup(
        schemas: str,
        semester: str,
        session: str,
        moyenne: float,
        credit: int,
        uuid_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")

    all_note = crud.note.read_note_by_moyenne_and_credit_sup(schemas, semester, journey.abbreviation, session, moyenne,
                                                             credit)
    return all_note


@router.get("/get_by_matier", response_model=schemas.Resultat)
def get_by_matier(
        semester: str,
        session: str,
        value_matier: str,
        uuid_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    validation = False
    all_columns = crud.note.check_columns_exist(schemas=schemas, semester=semester, journey=journey.abbreviation,
                                                session=session)
    for value in all_columns:
        if value == value_matier:
            validation = True

    if not validation:
        raise HTTPException(status_code=400, detail="matier value not found")
    all_note = {}
    non_valide = crud.note.read_note_failed(schemas, semester, journey.abbreviation, session, value_matier)
    valide = crud.note.read_note_succes(schemas, semester, journey.abbreviation, session, value_matier)
    all_note['list_valide'] = valide
    all_note['list_non_valide'] = non_valide
    return all_note


@router.get("/get_by_matier_pdf", response_model=List[Any])
def get_by_matier_pdf(
        college_year: str,
        semester: str,
        uuid_journey: str,
        session: str,
        value_ue: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    matier_ue = crud.teaching_unit.get_by_value(db=db, value=value_ue, semester=semester,
                                            uuid_journey=uuid_journey)
    if not matier_ue:
        raise HTTPException(status_code=400, detail="value ue not found")
    value_matier = []
    titre_note = []
    value_matier.append(f"ue_{value_ue}")
    titre_note.append("N° Carte")
    titre_note.append(matier_ue.title)
    value_ec = crud.constituent_element.get_by_value_ue(db=db, value_ue=value_ue, semester=semester,
                                                        uuid_journey=uuid_journey)
    for ec in value_ec:
        value_matier.append(f"ec_{ec.value}")
        titre_note.append(ec.title)

    titre_note.append("Crédit")
    titre_note.append("Status")
    matier = ','.join(tuple(value_matier))
    notes = []
    mention = crud.mention.get_by_uuid(db=db, uuid=journey.uuid_mention)
    all_note = crud.note.read_note_by_ue(semester, journey.abbreviation.lower(), session, matier)
    etudiant_admis = []
    etudiant_admis_compense = []
    for note in jsonable_encoder(all_note):

        etudiants = {'N° Carte': note["num_carte"], matier_ue.title: note[f"ue_{value_ue}"]}
        for ec in value_ec:
            etudiants[ec.title] = note[f"ec_{ec.value}"]
        if note[f"ue_{value_ue}"]:
            etudiants['Crédit'] = get_credit(float(note[f"ue_{value_ue}"]), matier_ue.credit)
            etudiants['Status'] = get_status(float(note[f"ue_{value_ue}"]))
            if note[f"ue_{value_ue}"] >= 10:
                info_etudiants = {'N° Carte': note["num_carte"]}
                un_etudiant = crud.ancien_student.get_by_num_carte(db=db, num_carte=note['num_carte'])
                info_etudiants['nom'] = un_etudiant.last_name
                info_etudiants['prenom'] = un_etudiant.first_name
                etudiant_admis.append(info_etudiants)
        else:
            etudiants['Crédit'] = get_credit(float(0), matier_ue.credit)
            etudiants['Status'] = get_status(float(0))

        if session.lower() == "rattrapage":
            if note[f"ue_{value_ue}"] is not None and note[f"ue_{value_ue}"] < 10:
                validation = crud.validation.get_by_num_carte(db=db, num_carte=note["num_carte"])
                if validation:
                    info_etudiants = {'N° Carte': note["num_carte"]}
                    un_etudiant = crud.ancien_student.get_by_num_carte(db=db, num_carte=note['num_carte'])
                    info_etudiants['nom'] = un_etudiant.last_name
                    info_etudiants['prenom'] = un_etudiant.first_name
                    etudiant_admis_compense.append(info_etudiants)
        notes.append(etudiants)
    data = {'mention': mention.title, 'journey': journey.title, 'anne': college_year, 'session': session}
    file = result_by_ue.PDF.create_result_by_ue(semester, journey, data, list(titre_note), notes, etudiant_admis,
                                                etudiant_admis_compense)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/get_by_session")
def get_by_sessiondefinitive_pdf(
        schema: str,
        semester: str,
        uuid_journey: str,
        session: str,
        type_result: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f" journey not found.", )

    mention = crud.mention.get_by_uuid(db=db, uuid=journey.uuid_mention)
    credit = 30
    if type_result == "definitive":
        all_note = crud.note.read_note_by_credit(schema, semester, journey.abbreviation.lower(), session, credit)
    else:
        all_note = crud.note.read_note_by_credit_inf(schema, semester, journey.abbreviation.lower(), session, credit)
    print(all_note)
    etudiant_admis = []
    for note in jsonable_encoder(all_note):
        validation = crud.semetre_valide.get_by_num_carte(schema=schema, num_carte=note["num_carte"])
        if validation:
            if test_semester(validation.semester, semester):
                info_etudiants = {'N° Carte': note["num_carte"]}
                un_etudiant = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=note['num_carte'])
                info_etudiants['nom'] = un_etudiant["nom"]
                info_etudiants['prenom'] = un_etudiant["prenom"]
                etudiant_admis.append(info_etudiants)
    data = {'mention': mention.title, 'journey': journey.title, 'anne': decode_schemas(schema), 'session': session}
    file = result_by_session.PDF.create_result_by_session(semester, journey, data, etudiant_admis, type_result)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)
