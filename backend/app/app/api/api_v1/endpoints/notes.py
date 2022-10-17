import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps
from app.utils import compare_list, create_anne, max_value, get_credit

from app.script_logging import ScriptLogging

router = APIRouter()


@router.post("/", response_model=Any)
def create_table_note(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        session: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """

    if crud.user.is_superuser(current_user):
        matiers = []
        journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
        if not journey:
            raise HTTPException(status_code=400, detail="journey not found")

        if semester not in journey.semester:
            raise HTTPException(status_code=400, detail="semester not found in journey")

        ues = crud.matier_ue.get_by_class(schema=create_anne(schema), uuid_journey=uuid_journey,
                                          semester=semester)
        for index, ue in enumerate(ues):
            matiers.append("ue_" + ue[2])
            ecs = crud.matier_ec.get_by_value_ue(schema=create_anne(schema), value_ue=ue[2], semester=semester,
                                                 uuid_journey=uuid_journey)
            for index_2, ec in enumerate(ecs):
                matiers.append("ec_" + ec[2])
        sesions = ["normal", "rattrapage", "final"]
        for session in sesions:
            test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                                    session=session)
            print(test_note)
            if not test_note:
                models.note.create_table_note(schema=create_anne(schema), journey=journey.abbreviation, semester=semester,
                                              matiers=matiers, session=session)
            else:
                all_columns = crud.note.check_columns_exist(schema=create_anne(schema), semester=semester,
                                                            journey=journey.abbreviation, session=session)
                matier = compare_list(matiers, all_columns)
                if len(matier) != 0:
                    models.note.update_table_note(schema=create_anne(schema), journey=journey.abbreviation, semester=semester,
                                                  matiers=matiers, session=session)
                else:
                    return crud.note.check_columns_exist(schema=create_anne(schema), semester=semester,
                                                         journey=journey.abbreviation,
                                                         session=session.lower())
        test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                                session=session.lower())
        if test_note:
            return crud.note.check_columns_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                                 session=session.lower())

    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.delete("/", response_model=schemas.Msg)
def delete_table_note(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
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
        test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                                session=session)
        if test_note:
            if models.note.drop_table_note(schema=create_anne(schema), journey=journey.abbreviation, session=session,
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
        schema: str,
        semester: str,
        session: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")
    test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                            session=session)
    if test_note:
        return crud.note.check_columns_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                             session=session)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
        )

@router.post("/insert_students/", response_model=List[Any])
def inserts_student(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        session: str,
        uuid_journey: str,
        uuid_mention: str,
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


    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail="mention not found")

    all_note = []
    test_note = crud.note.check_table_exist(create_anne(schema), semester, journey.abbreviation, session)
    if not test_note:
        raise HTTPException(
            status_code=400,
            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
        )

    if session.lower() == "rattrapage":
        test_note = crud.note.check_table_exist(create_anne(schema), semester, journey.abbreviation, "normal")
        if not test_note:
            raise HTTPException(status_code=400,
                                detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_normal not found.",
                                )
        credit = 30
        all_student = crud.note.read_by_credit(create_anne(schema), semester, journey.abbreviation, "normal", credit)
        for student in all_student:
            et_un = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, session, student.num_carte)
            if not et_un:
                crud.note.insert_note(create_anne(schema), semester, journey.abbreviation, session, student.num_carte)
                crud.note.update_auto(create_anne(schema), semester, journey.abbreviation, session, student.num_carte)
        all_note = crud.note.read_all_note(create_anne(schema), semester, journey.abbreviation, session)
        return all_note

    else:
        students = crud.ancien_student.get_by_class(db=db,college_year=schema,uuid_mention=uuid_mention,
                                                    uuid_journey= uuid_journey, semester=semester)
        print(len(students), semester)
        if students is not None:
            for student in students:
                et_un = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, session,
                                                    student.num_carte)
                if not et_un:
                    crud.note.insert_note(create_anne(schema), semester, journey.abbreviation, session, student.num_carte)
                    crud.note.insert_note(create_anne(schema), semester, journey.abbreviation, "final", student.num_carte)
        all_note = crud.note.read_all_note(create_anne(schema), semester, journey.abbreviation, session)
        return all_note


@router.get("/get_all_notes/", response_model=List[Any])
def get_all_notes(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        session: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    college_year = crud.college_year.get_by_title(db, schema)
    if not college_year:
        raise HTTPException(status_code=400, detail=f"{schema} not found.",
                            )

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(status_code=400, detail="journey not found")

    all_note = crud.note.read_all_note(create_anne(schema), semester, journey.abbreviation, session)
    return all_note


@router.post("/insert_note", response_model=Any)
def updates_note(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        semester: str,
        session: str,
        uuid_journey: str,
        all_notes_ue: schemas.Note,
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
    test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                            session=session)
    if not test_note:
        raise HTTPException(status_code=400,
                            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
                            )
    moy_cred_in = {}
    moy_cred_in_fin = {}
    #for notes in all_notes_ue:
    for note in all_notes_ue.ue:
        et_un = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, session, all_notes_ue.num_carte)
        et_un_final = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, "final", all_notes_ue.num_carte)
        if et_un:
            ue_in = {}
            ue_in_final = {}
            ecs = crud.matier_ec.get_by_value_ue(create_anne(schema), note.name, semester, uuid_journey)
            note_ue = 0
            note_ue_final = 0
            credit = crud.matier_ue.get_by_value(create_anne(schema), note.name, semester, uuid_journey).credit
            if len(note.ec) != len(ecs):
                raise HTTPException(status_code=400, detail="ivalide EC for UE",
                                    )
            for i, ec in enumerate(ecs):
                ec_note = note.ec[i].note
                if ec_note == "" or ec_note is None:
                    note.ec[i].note = None
                    value_ec_note = 0
                else:
                    value_ec_note = float(note.ec[i].note)

                value_sess = et_un_final[f'ec_{note.ec[i].name}']
                if value_sess is None:
                    value_sess = 0
                weight_ec = crud.matier_ec.get_by_value(create_anne(schema), ecs[i][2], semester, uuid_journey)
                note_ue += value_ec_note * float(weight_ec.weight)
                note_ue_final += max_value(value_ec_note, value_sess) * float(weight_ec.weight)
            ue_in[f'ue_{note.name}'] = note_ue
            ue_in_final[f'ue_{note.name}'] = note_ue_final
            for note_ec in note.ec:
                value_sess = et_un_final[f'ec_{note_ec.name}']
                if value_sess is None:
                    value_sess = 0
                ue_in[f'ec_{note_ec.name}'] = note_ec.note
                ue_in_final[f'ec_{note_ec.name}'] = max_value(note_ec.note, value_sess)
                print(max_value(note_ec.note, value_sess))

            crud.note.update_note(create_anne(schema), semester, journey.abbreviation, session, all_notes_ue.num_carte, ue_in)
            crud.note.update_note(create_anne(schema), semester, journey.abbreviation, "final", all_notes_ue.num_carte, ue_in_final)
            et_un = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, session, all_notes_ue.num_carte)
            et_un_final = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, "final",
                                                      all_notes_ue.num_carte)
            ues = crud.matier_ue.get_by_class(create_anne(schema), uuid_journey, semester)
            moy = 0
            credit = 0
            moy_fin = 0
            credit_fin = 0
            somme = 0
            for ue in ues:
                value_sess = et_un[f'ue_{ue.value}']
                if value_sess is None:
                    value_sess = 0
                value_fin = et_un_final[f'ue_{ue.value}']
                if value_fin is None:
                    value_fin = 0
                somme += ue.credit
                moy += float(value_sess) * ue.credit
                credit += get_credit(float(value_sess), ue.credit)

                moy_fin += float(value_fin) * ue.credit
                credit_fin += get_credit(float(value_fin), ue.credit)

                moy_cred_in["moyenne"] = moy / somme
                moy_cred_in["credit"] = credit

                moy_cred_in_fin["moyenne"] = moy_fin / somme
                moy_cred_in_fin["credit"] = credit_fin

                crud.note.update_note(create_anne(schema), semester, journey.abbreviation, session, all_notes_ue.num_carte, moy_cred_in)
                crud.note.update_note(create_anne(schema), semester, journey.abbreviation, "final", all_notes_ue.num_carte, moy_cred_in)
    note_student = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, session, all_notes_ue.num_carte)
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
        result = {"info": stud}
        sessions = ['Normal', 'Rattrapage']

        for session in sessions:
            test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester,
                                                    journey=journey.abbreviation,
                                                    session=session)
            if not test_note:
                raise HTTPException(status_code=400,
                                    detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
                                    )
            note_session = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, session,
                                                   num_carte)
            result[session]= note_session
        return result
    else:
        raise HTTPException(status_code=400, detail="Student not found.")



@router.delete("/student", response_model=List[Any])
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
    test_note = crud.note.check_table_exist(schema=create_anne(schema), semester=semester, journey=journey.abbreviation,
                                            session=session)
    if not test_note:
        raise HTTPException(status_code=400,
                            detail=f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()} not found.",
                            )
    et_un = crud.note.read_by_num_carte(create_anne(schema), semester, journey.abbreviation, session, num_carte)
    if et_un:
        print(num_carte)
        crud.note.delete_by_num_carte(create_anne(schema), semester, journey.abbreviation, session, et_un.num_carte)
    all_note = crud.note.read_all_note(create_anne(schema), semester, journey.abbreviation, session)
    return all_note
