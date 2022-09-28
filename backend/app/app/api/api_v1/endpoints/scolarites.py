from app import crud
from app.core.config import settings
from app.utils import get_niveau, decode_schemas, creaate_registre, validation_semester, create_anne
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from typing import Any
from app.api import deps
from fastapi.responses import FileResponse
from datetime import date
from app.utils_sco.scolarite import create_certificat_scolarite
from app.utils_sco.relever import PDF
from app.utils_sco.inscription import attestation_inscription
from app.utils_sco.credit import attestation_validation_credit
from app.utils_sco.assiduite import create_certificat_assidute

router = APIRouter()


@router.get("/certificat")
def certificat(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if student:
        journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey).title
        mention = crud.mention.get_by_uuid(db=db, uuid=student.uuid_mention).title
        data = {'last_name': student.last_name, 'first_name': student.first_name, 'date_birth': student.date_birth,
                'place_birth': student.place_birth,
                'level': get_niveau(student.inf_semester, student.sup_semester), 'mention': mention,
                'journey': journey, 'register': creaate_registre(student.actual_years)}
        date_ = date.today()
        anne = student.actual_years
        file = create_certificat_scolarite(num_carte, date_.year, anne, data)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")


@router.get("/attestation_inscription")
def attestation(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if student:
        journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey).title
        mention = crud.mention.get_by_uuid(db=db, uuid=student.uuid_mention).title
        data = {'last_name': student.last_name, 'first_name': student.first_name, 'date_birth': student.date_birth,
                'place_birth': student.place_birth,
                'level': get_niveau(student.inf_semester, student.sup_semester), 'mention': mention,
                'journey': journey, 'register': creaate_registre(student.actual_years)}
        date_ = date.today()
        anne = student.actual_years
        file = attestation_inscription(num_carte, date_.year, anne, data)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")


@router.get("/validation_credit")
def attestation_validation(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        level: str = "actual",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if student:
        journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey).title
        mention = crud.mention.get_by_uuid(db=db, uuid=student.uuid_mention).title
        new_level = get_niveau(student.inf_semester, student.sup_semester)
        data = {'last_name': student.last_name, 'first_name': student.first_name, 'date_birth': student.date_birth,
                'place_birth': student.place_birth,
                'level': new_level,
                'mention': mention,
                'journey': journey,
                'register': creaate_registre(student.actual_years)}
        date_ = date.today()
        if level != "actual" and level != new_level and level in settings.LEVEL:
            data['level'] = level
        file = attestation_validation_credit(num_carte, date_.year, data)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")


@router.get("/assiduite")
def certificat_assiduite(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        date_enter: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if student:
        journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey).title
        mention = crud.mention.get_by_uuid(db=db, uuid=student.uuid_mention).title
        data = {'last_name': student.last_name, 'first_name': student.first_name, 'date_birth': student.date_birth,
                'place_birth': student.place_birth,
                'level': get_niveau(student.inf_semester, student.sup_semester), 'mention': mention,
                'journey': journey, 'register': creaate_registre(student.actual_years)}
        date_ = date.today()
        file = create_certificat_assidute(num_carte, date_.year, date_enter, data, )
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")


@router.get("/relever")
def relever(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        college_year: str,
        semester: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    college_years = crud.college_year.get_by_title(db=db, title=college_year)
    if not college_years:
        raise HTTPException(status_code=400, detail=f"{college_year} not found.", )
    note = {}
    ue = {}
    ues = []
    session = "Normal"
    anne = college_year

    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if student:
        journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey).abbreviation
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    test_note = crud.note.check_table_exist(schemas=create_anne(college_year),
                                            semester=semester, journey=journey, session="rattrapage")
    test_note_final = crud.note.check_table_exist(schemas=create_anne(college_year),
                                                  semester=semester, journey=journey, session="final")
    if test_note:
        et_un_rattrapage = crud.note.read_by_num_carte(create_anne(college_year), semester, journey, "rattrapage", num_carte)
        if et_un_rattrapage:
            session = "Rattrapage"

    if not test_note_final:
        raise HTTPException(status_code=400, detail=f"note_{semester}_{journey}_final not found.",
                            )
    et_un_final = crud.note.read_by_num_carte(create_anne(college_year), semester, journey, "final", num_carte)

    if et_un_final and student:
        validation = crud.semetre_valide.get_by_num_carte(schema=create_anne(college_year), num_carte=num_carte)

        matier_ues = crud.matier_ue.get_by_class(create_anne(college_year), student.uuid_journey, semester)
        note['num_carte'] = num_carte
        note['moyenne'] = et_un_final['moyenne']
        note['credit'] = et_un_final['credit']
        for matier_ue in matier_ues:
            ue['name'] = matier_ue['title']
            ue['note'] = et_un_final[f"ue_{matier_ue['value']}"]
            ue['credit'] = matier_ue['credit']
            matier_ecs = crud.matier_ec.get_by_value_ue(create_anne(college_year),
                                                        matier_ue['value'], semester, student.uuid_journey)

            ecs = []
            for matier_ec in matier_ecs:
                ec = {'name': matier_ec['title'], 'note': et_un_final[f"ec_{matier_ec['value']}"],
                      'poids': matier_ec['poids']}
                ecs.append(ec.copy())
            ue['ec'] = ecs
            ues.append(ue.copy())
        note['ue'] = ues
        test_validation = {}
        if validation:
            test_validation = validation_semester(validation, semester, et_un_final['credit'], 30, anne)
        else:
            test_validation['status'] = f"Étudiant(e) redoublé(e)."
            test_validation['code'] = False
            test_validation['anne'] = college_year
        journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey).title
        mention = crud.mention.get_by_uuid(db=db, uuid=student.uuid_journey).title
        data = {'last_name': student.last_name, 'first_name': student.first_name, 'date_birth': student.date_birth,
                'place_birth':student.place_birth, 'semester': semester, 'mention': mention,
                'journey': journey, 'session': session, 'validation': test_validation['status'],
                'code': test_validation['code'], 'anne': test_validation['anne']}
        date_ = date.today()
        file = PDF.relever_note(num_carte, date_.year, data, note)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")
