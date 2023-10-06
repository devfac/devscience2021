import ast
from typing import Any
import json
from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.api import deps
from fastapi.responses import FileResponse
from app.liste import liste_exams, liste_inscrit, liste_bourse, liste_select
from app import crud
from app.utils import decode_schemas, get_niveau, create_model, find_in_list, get_last_year
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/list_exam/")
def list_examen(
        college_year: str,
        semester: str,
        id_journey: str,
        id_mention: str,
        session: str,
        salle: str,
        skip: int = 1,
        limit: int = 1000,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """

    mention = crud.mention.get_by_id(db=db, uuid=id_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    journey = crud.journey.get_by_id(db=db, uuid=id_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f" Journey not found.", )

    interaction = crud.interaction.get_by_journey_and_year(
        db=db, id_journey=id_journey, college_year=college_year)
    interaction_value = jsonable_encoder(interaction)
    list_value = []
    for value in interaction_value[semester.lower()]:
        value = ast.literal_eval(value)
        list_value.append(value)
    interaction = jsonable_encoder(interaction)
    interaction[semester.lower()] = list_value
    columns = interaction[semester.lower()]
    print(create_model(columns))

    data = {}
    matiers = {}

    if len(columns) == 0:
        raise HTTPException(
            status_code=400,
            detail="Matiers not found.",
        )
    all_ue = []
    for ue in create_model(columns):
        ues_ = {'name': ue['title']}
        nbr = 0
        all_ec = []
        for ec in ue['ec']:
            ecs_ = {'name': ec['title']}
            nbr += 1
            all_ec.append(ecs_)
        ues_['nbr_ec'] = nbr
        ues_['ec'] = all_ec
        all_ue.append(ues_)
    matiers['ue'] = all_ue

    students = crud.note.read_all_note(journey=journey.abbreviation,session=session,year=college_year,
                                        semester=semester,skip=skip, limit=limit-skip)

    all_students = []
    if len(students) == 0:
        raise HTTPException(
            status_code=400,
            detail="Etudiants not found.",
        )
    for on_student in students:
        un_et = crud.ancien_student.get_by_num_carte(db=db, num_carte=on_student.num_carte)
        if un_et and find_in_list(un_et.actual_years, college_year) != -1:
            student = {"last_name": un_et.last_name,
                       "first_name": un_et.first_name,
                       "num_carte": un_et.num_carte}
            all_students.append(student)
    print(len(all_students))
    data['mention'] = mention.title
    data['journey'] = journey.title
    data['anne'] = college_year
    data['session'] = session
    data['salle'] = salle
    data['skip'] = skip + 1
    data['limit'] = limit
    file = liste_exams.PDF.create_list_examen(semester, journey.abbreviation, data, matiers, all_students)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/list_inscrit/")
def list_inscrit(
        college_year: str,
        semester: str,
        id_journey: str,
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
    journey = crud.journey.get_by_id(db=db, uuid=id_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f" Journey not found.", )

    mention = crud.mention.get_by_id(db=db, uuid=journey.id_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    students = crud.ancien_student.get_by_class(db=db, id_journey=id_journey, id_mention=journey.id_mention,
                                                semester=semester, )

    all_student = []
    for on_student in students:
        if find_in_list(on_student.actual_years, college_year) != -1:
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
        id_mention: str,
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
    mention = crud.mention.get_by_id(db=db, uuid=id_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f"Mention not found.",)
    students = crud.new_student.get_all_admis_by_mention(db=db, id_mention=id_mention, college_year=college_year)

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
        college_year: str,
        id_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste bourse
    
    """
    type_ = "Passant"
    all_data = {}
    all_journey = []
    mention = crud.mention.get_by_id(db=db, uuid=id_mention)
    if not mention:
        raise HTTPException(
            status_code=404,
            detail="The mention with this uuid does not exist in the system.",
        )
    journeys = crud.journey.get_by_mention(db=db, id_mention=id_mention)
    all_data['mention'] = mention.title
    for journey in journeys:
        journey_ = {"name": journey.title}
        l1 = []
        l2 = []
        l3 = []
        m1 = []
        m2 = []
        students_ = crud.ancien_student.get_by_journey_and_type(db=db,id_journey=journey.id, type_=type_)

        for student in students_:
            if find_in_list(student.actual_years, college_year) != -1:
                students = {"last_name": student.last_name, "first_name": student.first_name, "num_carte": student.num_carte}
                level = get_niveau(student.inf_semester, student.sup_semester)
                if level == "L1":
                    if get_last_year(student.baccalaureate_years, college_year):
                        l1.append(students)
                if level == "L2":
                    l2.append(students)
                if level == "L3":
                    l3.append(students)
                if level == "M1":
                    m1.append(students)
                if level == "M2":
                    m2.append(students)
        journey_["l1"] = l1
        journey_["l2"] = l2
        journey_["l3"] = l3
        journey_["m1"] = m1
        journey_["m2"] = m2
        all_journey.append(journey_)
    all_data['journey'] = all_journey
    all_data['year'] = college_year.title()

    file = liste_bourse.PDF.create_list_bourse(mention.title, all_data, type_)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/list_bourse_redoublant/")
def list_bourse_passant(
        college_year: str,
        id_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste bourse

    """
    type_ = "Redoublant"
    all_data = {}
    all_journey = []
    mention = crud.mention.get_by_id(db=db, uuid=id_mention)
    if not mention:
        raise HTTPException(
            status_code=404,
            detail="The mention with this uuid does not exist in the system.",
        )

    college_year = crud.college_year.get_by_title(db=db, title=college_year)
    if not college_year:
        raise HTTPException(
            status_code=404,
            detail="The college year with this uuid does not exist in the system.",
        )
    journeys = crud.journey.get_by_mention(db=db, id_mention=id_mention)
    all_data['mention'] = mention.title
    for journey in journeys:
        journey_ = {"name": journey.title}
        l1 = []
        l2 = []
        l3 = []
        m1 = []
        m2 = []
        students_ = crud.ancien_student.get_by_journey_and_type_and_mean(db=db,id_journey=journey.id, type_=type_,
                                                                         mean=college_year.mean)
        for student in students_:
            if find_in_list(student.actual_years, college_year) != -1:
                students = {"last_name": student.last_name, "first_name": student.first_name,
                            "num_carte": student.num_carte}
                level = get_niveau(student.inf_semester, student.sup_semester)
                if level == "L1":
                    l1.append(students)
                if level == "L2":
                    l2.append(students)
                if level == "L3":
                    l3.append(students)
                if level == "M1":
                    m1.append(students)
                if level == "M2":
                    m2.append(students)
        journey_["l1"] = l1
        journey_["l2"] = l2
        journey_["l3"] = l3
        journey_["m1"] = m1
        journey_["m2"] = m2
        all_journey.append(journey_)
    all_data['journey'] = all_journey
    all_data['year'] = college_year.title

    file = liste_bourse.PDF.create_list_bourse(mention.title, all_data, type_)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)

