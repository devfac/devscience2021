from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.api import deps
from fastapi.responses import FileResponse
from app.liste import liste_exams, liste_inscrit, liste_bourse, liste_select
from app import crud
from app.utils import decode_schemas, get_niveau, create_anne
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/list_exam/")
def list_examen(
        college_year: str,
        semester: str,
        uuid_journey: str,
        uuid_mention: str,
        session: str,
        salle: str,
        skip: int = 1,
        limit: int = 100,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """

    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f" Journey not found.", )
    college_years = crud.college_year.get_by_title(db, college_year)
    if not college_years:
        raise HTTPException(status_code=400, detail=f"{college_year} not found.",
                            )
    data = {}
    matiers = {}
    ues = crud.matier_ue.get_by_class(create_anne(college_year), uuid_journey, semester)
    if len(ues) == 0:
        raise HTTPException(
            status_code=400,
            detail="Matiers not fount.",
        )
    all_ue = []
    for ue in ues:
        ues_ = {'name': ue['title']}
        nbr = 0
        ecs = crud.matier_ec.get_by_value_ue(create_anne(college_year), ue['value'], semester, uuid_journey)
        all_ec = []
        for ec in ecs:
            ecs_ = {}
            nbr += 1
            ecs_['name'] = ec['title']
            all_ec.append(ecs_)
        ues_['nbr_ec'] = nbr
        ues_['ec'] = all_ec
        all_ue.append(ues_)
    matiers['ue'] = all_ue

    students = crud.ancien_student.get_by_class_limit(db=db, uuid_journey=uuid_journey,uuid_mention=uuid_mention,
                                                      semester=semester,college_year=college_year,
                                                      offset=skip, limit=limit)

    all_students = []
    if len(students) == 0:
        raise HTTPException(
            status_code=400,
            detail="Etudiants not fount.",
        )
    for on_student in students:
        un_et = crud.note.read_by_num_carte(create_anne(college_year),
                                            semester, journey.abbreviation, session, on_student.num_carte)
        if un_et:
            student = {"last_name": on_student.last_name,
                       "first_name": on_student.first_name,
                       "num_carte": on_student.num_carte}
            all_students.append(student)

    data['mention'] = mention.title
    data['journey'] = journey.title
    data['anne'] = college_year
    data['session'] = session
    data['salle'] = salle
    data['skip'] = skip
    data['limit'] = limit
    file = liste_exams.PDF.create_list_examen(semester, journey.abbreviation, data, matiers, all_students)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/list_inscrit/")
def list_inscrit(
        college_year: str,
        semester: str,
        uuid_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """
    college_years = crud.college_year.get_by_title(db=db, title=college_year)
    if not college_years:
        raise HTTPException(status_code=400, detail=f"{college_year} not found.",
                            )
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f" Journey not found.", )

    students = crud.ancien_student.get_by_class(db=db, uuid_journey=uuid_journey,
                                                semester=semester, college_year=college_year)

    mention = crud.mention.get_by_uuid(db=db, uuid=journey.uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    all_student = []
    if students:
        for on_student in students:
            student = {"last_name": on_student.last_name,
                       "first_name": on_student.first_name,
                       "num_carte": on_student.num_carte}
            all_student.append(student)

    data = {'mention': mention.title, 'journey': journey.title, 'anne': college_year}
    file = liste_inscrit.PDF.create_list_inscrit(semester, journey.abbreviation, data, all_student)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/list_selection/")
def list_selection(
        college_year: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """
    college_years = crud.college_year.get_by_title(db=db, title=college_year)
    if not college_years:
        raise HTTPException(status_code=400, detail=f"{college_year} not found.",
                            )
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f"Mention not found.",)
    students = crud.new_student.get_all_admis_by_mention(db=db, uuid_mention=uuid_mention, college_year=college_year)

    level = ["L1", "M1", "M2"]
    all_students = {}
    if students:
        for lev in level:
            student_lev = []
            for on_student in students:
                student = {"last_name": on_student.last_name,
                           "first_name": on_student.first_name,
                           "num_select": on_student.num_select}
                if on_student.level == lev:
                    student_lev.append(student)

            all_students[lev] = student_lev

    data = {'mention': mention.title, 'anne': college_year}

    file = liste_select.PDF.create_list_select(mention.title, data, all_students)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/list_bourse_passant/")
def list_bourse_passant(
        schema: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",
                            )
    etat = "Passant"
    all_data = {}
    all_journey = []
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(
            status_code=404,
            detail="The mention with this uuid does not exist in the system.",
        )
    journey = crud.journey.get_by_mention(db=db, uuid_mention=uuid_mention)
    all_data['mention'] = mention.title
    for parcour in journey:
        journey_ = {}
        journey_["name"] = parcour.title
        l1 = []
        l2 = []
        l3 = []
        m1 = []
        m2 = []
        etudiants_ = crud.ancien_etudiant.get_by_journey_and_etat(schema=schema, uuid_journey=str(parcour.uuid),
                                                                   etat=etat)
        if etudiants_:
            for etudiant in etudiants_:
                etudiants = {}
                etudiants["nom"] = etudiant["nom"]
                etudiants["prenom"] = etudiant["prenom"]
                etudiants["num_carte"] = etudiant["num_carte"]
                niveau = get_niveau(etudiant['semester_petit'], etudiant['semester_grand'])
                if niveau == "L1":
                    l1.append(etudiants)
                if niveau == "L2":
                    l2.append(etudiants)
                if niveau == "L3":
                    l3.append(etudiants)
                if niveau == "M1":
                    m1.append(etudiants)
                if niveau == "M2":
                    m2.append(etudiants)
        journey_["l1"] = l1
        journey_["l2"] = l2
        journey_["l3"] = l3
        journey_["m1"] = m1
        journey_["m2"] = m2
        all_journey.append(journey_)
    all_data['parcour'] = all_journey
    all_data['anne'] = decode_schemas(schema)

    file = liste_bourse.PDF.create_list_bourse(mention.title, all_data, etat)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/list_bourse_redoublant/")
def list_bourse_redoublant(
        schema: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.",
                            )
    etat = "Redoublant"
    all_data = {}
    all_journey = []
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(
            status_code=404,
            detail="The mention with this uuid does not exist in the system.",
        )
    journey = crud.journey.get_by_mention(db=db, uuid_mention=uuid_mention)
    all_data['mention'] = mention.title
    for parcour in journey:
        journey_ = {}
        journey_["name"] = parcour.title
        l1 = []
        l2 = []
        l3 = []
        m1 = []
        m2 = []
        etudiants_ = crud.ancien_etudiant.get_by_journey_and_etat_and_moyenne(schema=schema,
                                                                               uuid_journey=str(parcour.uuid),
                                                                               etat=etat,
                                                                               moyenne=float(anne_univ.moyenne))
        if etudiants_:
            for etudiant in etudiants_:
                etudiants = {}
                etudiants["nom"] = etudiant["nom"]
                etudiants["prenom"] = etudiant["prenom"]
                etudiants["num_carte"] = etudiant["num_carte"]
                niveau = get_niveau(etudiant['semester_petit'], etudiant['semester_grand'])
                if niveau == "L1":
                    l1.append(etudiants)
                if niveau == "L2":
                    l2.append(etudiants)
                if niveau == "L3":
                    l3.append(etudiants)
                if niveau == "M1":
                    m1.append(etudiants)
                if niveau == "M2":
                    m2.append(etudiants)
        journey_["l1"] = l1
        journey_["l2"] = l2
        journey_["l3"] = l3
        journey_["m1"] = m1
        journey_["m2"] = m2
        all_journey.append(journey_)
    all_data['parcour'] = all_journey
    all_data['anne'] = decode_schemas(schema)

    file = liste_bourse.PDF.create_list_bourse(mention.title, all_data, etat)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)
