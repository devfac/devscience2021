import os
from typing import Any, List

from app import crud
from app import models
from app import schemas
from app.api import deps
from app.excel_code import save_data
from app.utils import check_table_info, check_columns_exist, decode_schemas, check_table_note, \
    get_credit, max_value, excel_to_model, transpose
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/get_models/")
def get_models(
        *,
        db: Session = Depends(deps.get_db),
        model_name: str = "student",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    """
    all_table = check_table_info("public")
    for table in all_table:
        if table == model_name:
            save_data.create_workbook(model_name, [model_name], "models")
            columns = check_columns_exist("public", table)
            save_data.write_data_title(table, table, columns, "models")

    return {"msg": "succes"}


@router.get("/get_models_notes/")
def get_models_notes(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid_journey: str,
        session: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )
    all_table_note = check_table_note(schema)
    parcour = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not parcour:
        raise HTTPException(status_code=400, detail=f" journey not found.", )
    file = None
    save_data.create_workbook(f"note_{parcour.abbreviation.lower()}_{session.lower()}", parcour.semester, "notes")
    for sems in parcour.semester:
        for table in all_table_note:
            if f"note_{parcour.abbreviation.lower()}_{sems.lower()}_{session.lower()}" == table:
                colums = check_columns_exist(schema, table)
                save_data.write_data_title(f"note_{parcour.abbreviation.lower()}_{session.lower()}", sems, colums,
                                           "notes")
                all_data = crud.save.read_all_data(schema, table)
                if all_data:
                    file = save_data.insert_data_xlsx(f"note_{parcour.abbreviation.lower()}_{session.lower()}",
                                                      sems, all_data, colums, "notes")
                    print("file", file)
                    return FileResponse(path=file, media_type='application/octet-stream', filename=file)
                else:
                    pass


@router.post("/insert_data/", response_model=List[Any])
def insert_from_xlsx(*,
                     file: UploadFile = File(...),
                     current_user: models.User = Depends(deps.get_current_active_user),
                     ) -> Any:
    """
    """
    all_data = save_data.get_data_xlsx(file.filename, "student")
    return all_data


@router.post("/uploadfile/")
async def create_upload_file(*,
                             uploaded_file: UploadFile = File(...),
                             model_name: str = "student",
                             college_year: str,
                             uuid_mention: str,
                             uuid_journey: str = "",
                             db: Session = Depends(deps.get_db),
                             current_user: models.User = Depends(deps.get_current_active_user)
                             ):
    file_location = f"files/excel/uploaded/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    all_data = []
    all_table = check_table_info("public")
    for table in all_table:
        if table == model_name:
            valid = save_data.validation_file(file_location, table, "public")
            if valid != "valid":
                raise HTTPException(
                    status_code=400,
                    detail=valid
                )
            all_data = save_data.get_data_xlsx(file_location, table)
    for data in all_data:
        data_ = jsonable_encoder(data)
        data_["uuid_mention"] = uuid_mention
        data_["uuid_journey"] = uuid_journey
        data_["actual_years"] = [college_year]
        data_["receipt"] = ""
        data_["mean"] = 10
        data_["receipt_list"] = []
        student = crud.ancien_student.get_by_num_carte(db=db, num_carte=data["num_carte"])
        new_student = schemas.NewStudentCreate(**data_)
        print(jsonable_encoder(new_student))
        if not student:
            crud.new_student.create(db=db, obj_in=new_student)
    os.remove(file_location)
    response = schemas.ResponseData(**{'count': len(all_data), 'data': all_data})
    return response


@router.post("/upload_note_file/")
async def create_upload_note_file(
        *,
        db: Session = Depends(deps.get_db),
        uploaded_file: UploadFile = File(...),
        schema: str,
        uuid_journey: str,
        session: str,
        semester: str,
        current_user: models.User = Depends(deps.get_current_active_user)
):
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )

    file_location = f"files/excel/uploaded/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    journey = crud.journey.get_by_uuid(db=db, uuid=uuid_journey)
    if not journey:
        raise HTTPException(
            status_code=400,
            detail="journey not found"
        )

    all_semester = journey.semester
    all_sheet = save_data.get_all_sheet(file_location)
    for i in range(len(all_semester)):
        if str(all_semester[i]) != str(all_sheet[i]):
            raise HTTPException(
                status_code=400,
                detail=f"invalide file {all_sheet[i]}",
            )
    test_note = crud.note.check_table_exist(schemas=schema, semester=semester, journey=journey.abbreviation,
                                            session=session)
    if test_note:
        table = f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()}"
        valid = save_data.validation_file_note(file_location, semester, table, schema)
        if valid != "valid":
            raise HTTPException(
                status_code=400,
                detail=valid
            )
        all_data = save_data.get_data_xlsx_note(file_location, semester)
        all_notes_ue = transpose(excel_to_model(all_data))
        moy_cred_in = {}
        moy_cred_in_fin = {}
        for notes in all_notes_ue:
            for note in notes:
                try:
                    note = schemas.Note(**note)
                    et_un = crud.note.read_by_num_carte(schema, semester, journey.abbreviation, session, note.num_carte)
                    et_un_final = crud.note.read_by_num_carte(schema, semester, journey.abbreviation, "final",
                                                              note.num_carte)
                    print("eto", et_un)
                    if et_un:
                        print("avy eo eto", et_un)
                        ue_in = {}
                        ue_in_final = {}
                        ecs = crud.matier_ec.get_by_value_ue(schema, note.name, semester, uuid_journey)
                        note_ue = 0
                        note_ue_final = 0
                        if len(note.ec) != len(ecs):
                            raise HTTPException(status_code=400, detail="ivalide EC for UE",
                                                )
                        for i, ec in enumerate(ecs):
                            ec_note = note.ec[i].note
                            if ec_note == "":
                                note.ec[i].note = None
                                value_ec_note = 0
                            else:
                                value_ec_note = float(note.ec[i].note)

                            value_sess = et_un_final[f'ec_{note.ec[i].name}']
                            if value_sess is None:
                                value_sess = 0
                            poids_ec = crud.matier_ec.get_by_value(schema, ecs[i][2], semester, uuid_journey)
                            note_ue += value_ec_note * float(poids_ec.poids)
                            note_ue_final += max_value(value_ec_note, value_sess) * float(poids_ec.poids)

                        print("farany eto", ue_in)
                        ue_in[f'ue_{note.name}'] = format(float(note_ue), '.30f')
                        ue_in_final[f'ue_{note.name}'] = format(float(note_ue_final), '.30f')
                        for note_ec in note.ec:
                            value_sess = et_un_final[f'ec_{note_ec.name}']
                            if value_sess is None:
                                value_sess = 0
                            ue_in[f'ec_{note_ec.name}'] = format(float(note_ec.note), '.30f')
                            ue_in_final[f'ec_{note_ec.name}'] = format(float(max_value(note_ec.note, value_sess)),
                                                                       '.30f')
                        crud.note.update_note(schema, semester, journey.abbreviation, session, note.num_carte, ue_in)
                        crud.note.update_note(schema, semester, journey.abbreviation, "final", note.num_carte,
                                              ue_in_final)
                        et_un = crud.note.read_by_num_carte(schema, semester, journey.abbreviation, session,
                                                            note.num_carte)
                        et_un_final = crud.note.read_by_num_carte(schema, semester, journey.abbreviation, "final",
                                                                  note.num_carte)
                        ues = crud.matier_ue.get_by_class(schema, uuid_journey, semester)
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

                            moy_cred_in["moyenne"] = format(moy / somme, '.4f')
                            moy_cred_in["credit"] = credit

                            moy_cred_in_fin["moyenne"] = format(moy_fin / somme, '.4f')
                            moy_cred_in_fin["credit"] = credit_fin

                            crud.note.update_note(schema, semester, journey.abbreviation, session, note.num_carte,
                                                  moy_cred_in)
                            crud.note.update_note(schema, semester, journey.abbreviation, "final", note.num_carte,
                                                  moy_cred_in)
                except Exception as e:
                    print("error", e)
                    continue
        all_note = crud.note.read_all_note(schema, semester, journey.abbreviation, session)
    os.remove(file_location)
    return all_note


@router.get("/save_data/")
def save_data_to_excel(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )
    all_table = check_table_info(schema)
    save_data.create_workbook(decode_schemas(schema=schema), all_table, "data")
    for table in all_table:
        colums = check_columns_exist(schema, table)
        save_data.write_data_title(decode_schemas(schema=schema), table, colums, "data")
        all_data = crud.save.read_all_data(schema, table)
        if all_data:
            save_data.insert_data_xlsx(decode_schemas(schema=schema), table, all_data, colums, "data")

    all_table = check_table_info("public")
    save_data.create_workbook("public", all_table, "data")
    for table in all_table:
        colums = check_columns_exist("public", table)
        save_data.write_data_title("public", table, colums, "data")
        all_data = crud.save.read_all_data("public", table)
        if all_data:
            save_data.insert_data_xlsx("public", table, all_data, colums, "data")
    return {"msg": "succes"}
