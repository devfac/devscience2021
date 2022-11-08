from app import crud
from app.core.config import settings
from app.utils import get_niveau, decode_schemas, creaate_registre, validation_semester, create_anne, create_model
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from typing import Any
from app.api import deps
from fastapi.responses import FileResponse
from datetime import date
from app.utils_sco.scolarite import create_certificat_scolarite
from app.utils_sco.relever import PDF, relever_note
from app.utils_sco.inscription import attestation_inscription
from app.utils_sco.credit import attestation_validation_credit
from app.utils_sco.assiduite import create_certificat_assidute
from fastapi.encoders import jsonable_encoder
import json

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
        uuid_journey: str,
        semester: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    note = {}
    session = "Normal"
    anne = college_year

    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f"Journey not found.")
    test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation, session="rattrapage")
    test_note_final = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation, session="final")
    if test_note:
        et_un_rattrapage = crud.note.read_by_num_carte(semester, journey.abbreviation, "rattrapage", num_carte)
        if et_un_rattrapage:
            session = "Rattrapage"

    if not test_note_final:
        raise HTTPException(status_code=400, detail=f"note_{semester}_{journey.abbreviation}_final not found.",
                            )
    et_un_final = crud.note.read_by_num_carte(semester, journey.abbreviation, "final", num_carte)

    if et_un_final and student:
        validation = crud.validation.get_by_num_carte(db=db, num_carte=num_carte)

        interaction = crud.interaction.get_by_journey_and_year(
            db=db, uuid_journey=journey.uuid, college_year=college_year)
        interaction_value = jsonable_encoder(interaction)
        list_value = []
        for value in interaction_value[semester.lower()]:
            value = value.replace("'", '"')
            value = json.loads(value)
            list_value.append(value)
        interaction = jsonable_encoder(interaction)
        interaction[semester.lower()] = list_value
        columns = interaction[semester.lower()]

        note['num_carte'] = num_carte
        note['mean'] = et_un_final['mean']
        note['credit'] = et_un_final['credit']

        all_ue = []
        for ue in create_model(columns):
            ues_ = {'name': crud.teaching_unit.get_by_value(db=db, value=ue['name'], uuid_journey=journey.uuid,
                                                            semester=semester).title,
                    'note':et_un_final[f"ue_{ue['name']}"],
                    'credit': ue['credit']
                    }
            all_ec = []
            for ec in ue['ec']:
                ecs_ = {
                    'name': crud.constituent_element.get_by_value(db=db, value=ec['name'], uuid_journey=journey.uuid,
                                                                  semester=semester).title,
                    'note':et_un_final[f"ec_{ec['name']}"],
                    'weight': ec['weight']
                }
                all_ec.append(ecs_)
            ues_['ec'] = all_ec
            all_ue.append(ues_)
        note['ue'] = all_ue

        test_validation = {}
        if validation:
            validation = jsonable_encoder(validation)
            test_validation = validation_semester(validation[semester.lower()], et_un_final['credit'], 30, anne)
        else:
            test_validation['status'] = f"Étudiant(e) redoublé(e)."
            test_validation['code'] = False
            test_validation['anne'] = college_year
        mention = crud.mention.get_by_uuid(db=db, uuid=student.uuid_mention).title
        data = {'last_name': student.last_name, 'first_name': student.first_name, 'date_birth': student.date_birth,
                'place_birth':student.place_birth, 'semester': semester, 'mention': mention,
                'journey': journey.title, 'session': session, 'validation': test_validation['status'],
                'code': test_validation['code'], 'anne': test_validation['anne']}
        date_ = date.today()
        file = relever_note(num_carte=num_carte, date=date_.year, data=data, note=note)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Student not found")
