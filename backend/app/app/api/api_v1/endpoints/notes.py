import json
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import compare_list, max_value, get_credit, create_model, find_in_list

router = APIRouter()


@router.post("/", response_model=Any)
def create_table_note(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        semester: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """

    if crud.user.is_superuser(current_user):
        journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
        if not journey:
            raise HTTPException(status_code=400, detail="journey not found")

        if semester not in journey.semester:
            raise HTTPException(status_code=400, detail="semester not found in journey")

        interaction = crud.interaction.get_by_journey_and_year(
                db=db, uuid_journey=uuid_journey,college_year=college_year)
        interaction_value = jsonable_encoder(interaction)
        list_value = []
        for value in interaction_value[semester.lower()]:
            value = value.replace("'", '"')
            value = json.loads(value)
            list_value.append(value)
        interaction = jsonable_encoder(interaction)
        interaction[semester.lower()] = list_value
        columns = interaction[semester.lower()]

        all_column = []
        for column in columns:
            all_column.append(f"{column['type']}_{column['name']}")
        sessions = ["normal", "rattrapage", "final"]
        for session in sessions:
            test_note = crud.note.check_table_exist( semester=semester, journey=journey.abbreviation,
                                                    session=session)
            if not test_note:
                models.note.create_table_note(journey=journey.abbreviation, semester=semester,
                                              matiers=all_column, session=session)
            else:
                all_columns = crud.note.check_columns_exist(semester=semester,
                                                            journey=journey.abbreviation, session=session)
                column_ = compare_list(all_column, all_columns)
                if len(column_) != 0:
                    models.note.update_table_note(journey=journey.abbreviation, semester=semester,
                                                  column=all_column, session=session)
        test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation,
                                                session=session.lower())
        if test_note:
            return crud.note.check_columns_exist(semester=semester, journey=journey.abbreviation,
                                                 session=session.lower())

    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.delete("/", response_model=schemas.Msg)
def delete_table_note(
        *,
        db: Session = Depends(deps.get_db),
        semester: str,
        uuid_journey: str,
        session: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
    if crud.user.is_superuser(current_user):

        journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
        if not journey:
            raise HTTPException(status_code=400, detail="journey not found")
        test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation,
                                                session=session.lower())
        if test_note:
            if models.note.drop_table_note(journey=journey.abbreviation, session=session,
                                           semester=semester):
                return {"msg": "Succces"}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
            )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.get("/", response_model=Any)
def get_all_columns(
        *,
        db: Session = Depends(deps.get_db),
        semester: str,
        session: str,
        uuid_journey: str,
        college_year,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation,
                                            session=session)

    interaction = crud.interaction.get_by_journey_and_year(
        db=db, uuid_journey=uuid_journey, college_year=college_year)
    interaction_value = jsonable_encoder(interaction)
    list_value = []
    if not interaction:
        raise HTTPException(
            status_code=400,
            detail=f"Matier_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
        )
    for value in interaction_value[semester.lower()]:
        value = value.replace("'", '"')
        value = json.loads(value)
        list_value.append(value)
    interaction = jsonable_encoder(interaction)
    interaction[semester.lower()] = list_value
    columns = interaction[semester.lower()]
    print(create_model(columns))
    all_ue = []
    for ue in create_model(columns):
        ues_ = {'name': crud.teaching_unit.get_by_value(db=db, value=ue['name'], uuid_journey=uuid_journey,
                                                        semester=semester).value}
        nbr = 0
        all_ec = []
        for ec in ue['ec']:
            ecs_ = {'name': crud.constituent_element.get_by_value(db=db, value=ec['name'], uuid_journey=uuid_journey,
                                                                  semester=semester).value}
            nbr += 1
            all_ec.append(ecs_)
        ues_['nbr_ec'] = nbr
        ues_['ec'] = all_ec
        all_ue.append(ues_)
    print(all_ue)
    if test_note:
        return all_ue
    else:
        raise HTTPException(
            status_code=400,
            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
        )

@router.get("/test_note", response_model=bool)
def get_exist_table(
        *,
        db: Session = Depends(deps.get_db),
        semester: str,
        session: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")

    return crud.note.check_table_exist(semester=semester, journey=journey.abbreviation,
                                            session=session)


@router.post("/insert_students/", response_model=schemas.ResponseData)
def inserts_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        semester: str,
        session: str,
        uuid_journey: str,
        uuid_mention: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")


    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail="mention not found")

    test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation, session=session)
    if not test_note:
        raise HTTPException(
            status_code=400,
            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
        )

    if session.lower() == "rattrapage":
        test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation, session="normal")
        if not test_note:
            raise HTTPException(status_code=400,
                                detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_normal not found.",
                                )
        credit = 30
        all_student = crud.note.read_by_credit(semester=semester, journey=journey.abbreviation,
                                               session="normal", credit=credit, year=college_year)
        for student in all_student:
                et_un = crud.note.read_by_num_carte(semester=semester, journey=journey.abbreviation,
                                                    session=session,num_carte=student.num_carte)
                if et_un:
                    year = {'year': college_year}
                    crud.note.update_note(semester=semester, journey=journey.abbreviation,
                                      session=session, num_carte=student.num_carte, ue_in=year)
                else:
                    crud.note.insert_note(semester=semester, journey=journey.abbreviation,
                                          session=session, num_carte=student.num_carte, year=college_year)
                    crud.note.update_auto(semester=semester, journey=journey.abbreviation,
                                          session=session, num_carte=student.num_carte)
        all_note = crud.note.read_all_note(semester=semester, journey=journey.abbreviation, session=session, year=college_year)
        all_note_ = []
        count = len(all_note)
        for note in all_note:
            note = jsonable_encoder(note)
            note['validation'] = False
            validation = crud.validation.get_by_num_carte(db=db, num_carte=note['num_carte'])
            if validation:
                validation = jsonable_encoder(validation)
                if validation[semester.lower()]:
                    note['validation'] = True
            all_note_.append(note)
        response = schemas.ResponseData(**{'count':count, 'data':all_note_})
        return response
    else:
        students = crud.ancien_student.get_by_class(db=db,uuid_mention=uuid_mention,
                                                    uuid_journey= uuid_journey, semester=semester)

        for student in students:
            if find_in_list(student.actual_years, college_year) != -1:
                et_un = crud.note.read_by_num_carte(semester=semester, journey=journey.abbreviation,
                                                    session=session,num_carte=student.num_carte)
                if et_un:
                    sessions = ['normal', 'final']
                    for session_ in sessions:
                        year = {'year': college_year}
                        crud.note.update_note(semester=semester, journey=journey.abbreviation,
                                          session=session_, num_carte=student.num_carte, ue_in=year)
                else:
                    sessions = ['normal', 'final']
                    for session_ in sessions:
                        crud.note.insert_note(semester=semester, journey=journey.abbreviation,
                                          session=session_, num_carte=student.num_carte, year=college_year)
        all_note = crud.note.read_all_note(semester=semester, journey=journey.abbreviation,
                                           session=session,  year=college_year)
        all_note_ = []
        count = len(all_note)
        for note in all_note:
            note = jsonable_encoder(note)
            note['validation'] = False
            validation = crud.validation.get_by_num_carte(db=db, num_carte=note['num_carte'])
            if validation:
                validation = jsonable_encoder(validation)
                if validation[semester.lower()]:
                    note['validation'] = True
            all_note_.append(note)
    response = schemas.ResponseData(**{'count':count, 'data':all_note_})
    return response



@router.get("/get_all_notes/", response_model=schemas.ResponseData)
def get_all_notes(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        semester: str,
        session: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")

    all_note = crud.note.read_all_note(semester=semester, journey=journey.abbreviation,
                                       session=session, year=college_year)
    all_note_ = []
    count = len(all_note)
    for note in all_note:
        note = jsonable_encoder(note)
        note['validation'] = False
        validation = crud.validation.get_by_num_carte(db=db, num_carte=note['num_carte'])
        if validation:
            validation = jsonable_encoder(validation)
            if validation[semester.lower()]:
                note['validation'] = True
        all_note_.append(note)

    response = schemas.ResponseData(**{'count':count, 'data':all_note_})
    return response


@router.post("/insert_note", response_model=Any)
def updates_note(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        semester: str,
        session: str,
        uuid_journey: str,
        all_notes_ue: schemas.Note,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation, session=session)
    if not test_note:
        raise HTTPException(status_code=400,
                            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
                            )
    interaction = crud.interaction.get_by_journey_and_year(
        db=db, uuid_journey=uuid_journey, college_year=college_year)
    interaction_value = jsonable_encoder(interaction)
    list_value = []
    for value in interaction_value[semester.lower()]:
        value = value.replace("'", '"')
        value = json.loads(value)
        list_value.append(value)
    interaction = jsonable_encoder(interaction)
    interaction[semester.lower()] = list_value
    columns = interaction[semester.lower()]
    print(create_model(columns))
    moy_cred_in = {}
    moy_cred_in_fin = {}
    moy = 0
    credit = 0
    moy_fin = 0
    credit_fin = 0
    somme = 0
    #for notes in all_notes_ue:
    for note in all_notes_ue.ue:
        for column_ in create_model(columns):
            if note.name == column_['name']:
                et_un = crud.note.read_by_num_carte(semester=semester, journey=journey.abbreviation,
                                                    session=session, num_carte=all_notes_ue.num_carte)
                et_un_final = crud.note.read_by_num_carte(semester=semester, journey=journey.abbreviation,
                                                    session='final', num_carte=all_notes_ue.num_carte)
                if et_un:
                    ue_in = {}
                    ue_in_final = {}
                    note_ue = 0
                    note_ue_final = 0
                    if len(note.ec) != len(column_['ec']):
                        raise HTTPException(status_code=400, detail="Invalid EC for UE", )
                    for i, ec in enumerate(column_['ec']):
                        ec_note = note.ec[i].note
                        if ec_note == "" or ec_note is None:
                            note.ec[i].note = None
                            value_ec_note = 0
                        else:
                            value_ec_note = float(note.ec[i].note)

                        value_sess = et_un_final[f"ec_{note.ec[i].name}"]
                        if value_sess is None:
                            value_sess = 0
                        note_ue += value_ec_note * float(ec['weight'])
                        note_ue_final += max_value(value_ec_note, value_sess) * float(ec['weight'])

                    ue_in[f'ue_{note.name}'] = note_ue
                    ue_in_final[f'ue_{note.name}'] = note_ue_final
                    for note_ec in note.ec:
                        value_sess = et_un_final[f'ec_{note_ec.name}']
                        if value_sess is None:
                            value_sess = 0
                        ue_in[f'ec_{note_ec.name}'] = note_ec.note
                        ue_in_final[f'ec_{note_ec.name}'] = max_value(note_ec.note, value_sess)
        
                    crud.note.update_note(semester, journey.abbreviation, session, all_notes_ue.num_carte, ue_in)
                    crud.note.update_note(semester, journey.abbreviation, "final", all_notes_ue.num_carte, ue_in_final)
                    et_un = crud.note.read_by_num_carte(semester, journey.abbreviation, session, all_notes_ue.num_carte)
                    et_un_final = crud.note.read_by_num_carte(semester, journey.abbreviation, "final",
                                                              all_notes_ue.num_carte)
                    value_sess = et_un[f'ue_{column_["name"]}']
                    print('value_sess', value_sess)
                    if value_sess is None:
                        value_sess = 0
                    value_fin = et_un_final[f'ue_{column_["name"]}']
                    if value_fin is None:
                        value_fin = 0
                    somme += column_["credit"]
                    moy += float(value_sess) * column_["credit"]
                    credit += get_credit(float(value_sess), column_["credit"])
                    print(get_credit(value_sess, column_['credit']))

                    moy_fin += float(value_fin) * column_["credit"]
                    credit_fin += get_credit(float(value_fin), column_["credit"])

                    moy_cred_in["mean"] = moy / somme
                    moy_cred_in["credit"] = credit

                    moy_cred_in_fin["mean"] = moy_fin / somme
                    moy_cred_in_fin["credit"] = credit_fin

                    crud.note.update_note(semester, journey.abbreviation, session, all_notes_ue.num_carte, moy_cred_in)
                    crud.note.update_note(semester, journey.abbreviation, "final", all_notes_ue.num_carte, moy_cred_in)
    note_student = crud.note.read_by_num_carte(semester, journey.abbreviation, session, all_notes_ue.num_carte)
    return note_student

@router.get("/view_details", response_model=Any)
def details_note(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid_journey: str,
        semester: str,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
):

    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.")

    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)

    if student:
        stud = schemas.AncienStudent(**jsonable_encoder(student))
        stud.journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey)
        mention = crud.mention.get_by_uuid(db=db, uuid=stud.journey.uuid_mention)
        stud.journey.mention = mention
        stud = jsonable_encoder(stud)
        stud['validation'] = False
        validation = crud.validation.get_by_num_carte(db=db, num_carte=num_carte)
        if validation:
            validation = jsonable_encoder(validation)
            if validation[semester.lower()]:
                stud['validation'] = True
        result = {"info": stud}
        sessions = ['Normal', 'Rattrapage']

        for session in sessions:
            test_note = crud.note.check_table_exist(semester=semester,
                                                    journey=journey.abbreviation,
                                                    session=session)
            if not test_note:
                raise HTTPException(status_code=400,
                                    detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
                                    )
            note_session = crud.note.read_by_num_carte(semester, journey.abbreviation, session,
                                                   num_carte)
            result[session]= note_session
        return result
    else:
        raise HTTPException(status_code=400, detail="Student not found.")



@router.delete("/student", response_model=schemas.ResponseData)
def delete_note(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        uuid_journey: str,
        num_carte: str,
        session: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.",
                            )

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation,
                                            session=session)
    if not test_note:
        raise HTTPException(status_code=400,
                            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
                            )
    et_un = crud.note.read_by_num_carte(semester, journey.abbreviation, session, num_carte)
    if et_un:
        crud.note.delete_by_num_carte(semester, journey.abbreviation, session, et_un.num_carte)
    all_note = crud.note.read_all_note(semester, journey.abbreviation, session)
    all_note_ = []
    count = len(all_note)
    for note in all_note:
        note = jsonable_encoder(note)
        note['validation'] = False
        validation = crud.validation.get_by_num_carte(db=db, num_carte=note['num_carte'])
        if validation:
            validation = jsonable_encoder(validation)
            if validation[semester.lower()]:
                note['validation'] = True
        all_note_.append(note)

    response = schemas.ResponseData(**{'count':count, 'data':all_note_})
    return response
