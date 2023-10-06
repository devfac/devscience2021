import os
import json
from typing import Any, List

from app import crud
from app import models
from app import schemas
from app.api import deps
from app.excel_code import save_data
from app.utils import check_table_info, check_columns_exist, decode_schemas, check_table_note, \
    get_credit, max_value, excel_to_model, transpose, create_model
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

    file = f'files/excel/models/{model_name}.xlsx'
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/get_models_notes/")
def get_models_notes(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        id_journey: str,
        semester: str,
        session: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    """
    all_table_note = check_table_note()
    journey = crud.journey.get_by_id(db=db, uuid=id_journey)
    if not journey:
        raise HTTPException(status_code=400, detail=f" journey not found.", )
    file = None
    for table in all_table_note:
        if f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()}" == table:

            interaction = crud.interaction.get_by_journey_and_year(
                db=db, id_journey=id_journey, college_year=college_year)
            interaction_value = jsonable_encoder(interaction)
            list_value = []
            for value in interaction_value[semester.lower()]:
                value = value.replace("'", '"')
                value = json.loads(value)
                list_value.append(value)
            interaction = jsonable_encoder(interaction)
            interaction[semester.lower()] = list_value
            columns = interaction[semester.lower()]
            all_column = ["num_carte"]
            for column in columns:
                all_column.append(f"{column['type']}_{column['name']}")
            print(all_column)
            save_data.create_workbook(f"note_{journey.abbreviation.lower()}_{session.lower()}", journey.semester, "note")
            save_data.write_data_title(f"note_{journey.abbreviation.lower()}_{session.lower()}", semester, all_column,
                                       "note")
            all_data = crud.save.read_all_data("public", table)
            if all_data:
                file = save_data.insert_data_xlsx(f"note_{journey.abbreviation.lower()}_{session.lower()}", semester, all_data, all_column, "note")
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
                             id_mention: str,
                             id_journey: str = "",
                             db: Session = Depends(deps.get_db),
                             current_user: models.User = Depends(deps.get_current_active_user)
                             ):
    file_location = f"files/excel/uploaded/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    all_data = []
    all_data_filter = []
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
        student = crud.ancien_student.get_by_num_carte(db=db, num_carte=data["num_carte"])
        if not student:
            data_ = jsonable_encoder(data)
            data_["id_mention"] = id_mention
            data_["id_journey"] = id_journey
            data_["actual_years"] = [college_year]
            data_["receipt"] = ""
            data_["mean"] = 10
            data_["receipt_list"] = []
            new_student = schemas.NewStudentUploaded(**data_)
            all_data_filter.append(new_student)
    os.remove(file_location)
    response = schemas.ResponseData(**{'count': len(all_data_filter), 'data': all_data_filter})
    return response


@router.post("/upload_note_file/")
async def create_upload_note_file(
        *,
        db: Session = Depends(deps.get_db),
        uploaded_file: UploadFile = File(...),
        college_year: str,
        id_journey: str,
        session: str,
        semester: str,
        current_user: models.User = Depends(deps.get_current_active_user)
):
    file_location = f"files/excel/uploaded/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    journey = crud.journey.get_by_id(db=db, uuid=id_journey)
    if not journey:
        raise HTTPException(
            status_code=400,
            detail="journey not found"
        )

    test_note = crud.note.check_table_exist(semester=semester, journey=journey.abbreviation, session=session)
    if test_note:
        table = f"note_{journey.abbreviation.lower()}_{semester.lower()}_{session.lower()}"

        interaction = crud.interaction.get_by_journey_and_year(
            db=db, id_journey=id_journey, college_year=college_year)
        interaction_value = jsonable_encoder(interaction)
        list_value = []
        for value in interaction_value[semester.lower()]:
            value = value.replace("'", '"')
            value = json.loads(value)
            list_value.append(value)
        interaction = jsonable_encoder(interaction)
        interaction[semester.lower()] = list_value
        columns = interaction[semester.lower()]
        all_column = ["num_carte"]
        for column in columns:
            all_column.append(f"{column['type']}_{column['name']}")

        valid = save_data.validation_file_note(file_location, semester, all_column)
        if valid != "valid":
            raise HTTPException(
                status_code=400,
                detail=valid
            )

        all_data = save_data.get_data_xlsx_note(file_location, semester)
        all_notes_ue = transpose(excel_to_model(all_data))

        all_note = []
        print(all_notes_ue)
        # return excel_to_model(all_data)
        for note_ue_ in excel_to_model(all_data):
            moy_cred_in = {}
            moy_cred_in_fin = {}
            moy = 0
            credit = 0
            moy_fin = 0
            credit_fin = 0
            somme = 0
            for note in note_ue_:
                try:
                    print(note)
                    note = schemas.NoteUE(**note)
                    for column_ in create_model(columns):
                        if note.name == column_['name']:
                            et_un = crud.note.read_by_num_carte(semester=semester, journey=journey.abbreviation,
                                                                session=session, num_carte=note.num_carte)
                            et_un_final = crud.note.read_by_num_carte(semester=semester, journey=journey.abbreviation,
                                                                      session='final', num_carte=note.num_carte)
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

                                ue_in[f'ue_{note.name}'] =format(note_ue, '.3f')
                                ue_in_final[f'ue_{note.name}'] = format(note_ue_final, '.3f')
                                for note_ec in note.ec:
                                    value_sess = et_un_final[f'ec_{note_ec.name}']
                                    if value_sess is None:
                                        value_sess = 0
                                    ue_in[f'ec_{note_ec.name}'] = note_ec.note
                                    ue_in_final[f'ec_{note_ec.name}'] = max_value(note_ec.note, value_sess)

                                crud.note.update_note(semester, journey.abbreviation, session, note.num_carte, ue_in)
                                crud.note.update_note(semester, journey.abbreviation, "final", note.num_carte,
                                                      ue_in_final)
                                et_un = crud.note.read_by_num_carte(semester, journey.abbreviation, session,
                                                                    note.num_carte)
                                et_un_final = crud.note.read_by_num_carte(semester, journey.abbreviation, "final",
                                                                          note.num_carte)
                                value_sess = et_un[f'ue_{column_["name"]}']
                                if value_sess is None:
                                    value_sess = 0
                                value_fin = et_un_final[f'ue_{column_["name"]}']
                                if value_fin is None:
                                    value_fin = 0
                                somme += column_["credit"]
                                moy += float(value_sess) * column_["credit"]
                                credit += get_credit(float(value_sess), column_["credit"])

                                moy_fin += float(value_fin) * column_["credit"]
                                credit_fin += get_credit(float(value_fin), column_["credit"])

                                moy_cred_in["mean"] = format(moy / somme, '.3f')
                                moy_cred_in["credit"] = credit

                                moy_cred_in_fin["mean"] = format(moy_fin / somme, '.3f')
                                moy_cred_in_fin["credit"] = credit_fin

                                crud.note.update_note(semester, journey.abbreviation, session, note.num_carte,
                                                      moy_cred_in)
                                crud.note.update_note(semester, journey.abbreviation, "final", note.num_carte,
                                                      moy_cred_in)
                except Exception as e:
                    print(e)
                    continue

            note_student = crud.note.read_by_num_carte(semester, journey.abbreviation, session, note_ue_[0]["num_carte"])
            all_note.append(note_student)
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
    college_year = crud.college_year.get_by_title(db, decode_schemas(schema=schema))
    if not college_year:
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
