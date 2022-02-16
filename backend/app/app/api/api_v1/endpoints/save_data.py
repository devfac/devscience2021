import os
from typing import Any, List

from app import crud
from app import models
from app.api import deps
from app.excel_code import save_data
from app.utils import check_table_info, create_anne, check_columns_exist, decode_schemas, check_table_note
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/get_models/")
def get_models(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    """
    anne_univ = crud.anne_univ.get_actual_value(db=db)
    all_table = check_table_info(create_anne(anne_univ.title))
    save_data.create_workbook(anne_univ.title, all_table, "models")
    for table in all_table:
        colums = check_columns_exist(create_anne(anne_univ.title), table)
        save_data.write_data_title(anne_univ.title, table, colums, "models")

    all_table = check_table_info("public")
    save_data.create_workbook("public", all_table, "models")
    for table in all_table:
        colums = check_columns_exist("public", table)
        save_data.write_data_title("public", table, colums, "models")

    all_table_note = check_table_note(create_anne(anne_univ.title))
    print(all_table_note)
    return {"msg": "succes"}


@router.get("/get_models_notes/")
def get_models_notes(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    """
    anne_univ = crud.anne_univ.get_actual_value(db=db)
    all_table_note = check_table_note(create_anne(anne_univ.title))
    sessions = ['normal', 'rattrapage', "final"]
    parcours = crud.parcours.get_multi(db=db)
    for session in sessions:
        for parcour in parcours:
            save_data.create_workbook(f"note_{parcour.abreviation.lower()}_{session.lower()}", parcour.semestre,
                                      "notes")
            for sems in parcour.semestre:
                for table in all_table_note:
                    if f"note_{parcour.abreviation.lower()}_{sems.lower()}_{session.lower()}" == table:
                        print("note", table)
                        colums = check_columns_exist(create_anne(anne_univ.title), table)
                        save_data.write_data_title(f"note_{parcour.abreviation.lower()}_{session.lower()}", sems,
                                                   colums, "notes")
                        all_data = crud.save.read_all_data(create_anne(anne_univ.title), table)
                        if all_data:
                            save_data.insert_data_xlsx(f"note_{parcour.abreviation.lower()}_{session.lower()}", sems,
                                                       all_data, colums, "notes")
    return {"msg": "succes"}


@router.post("/insert_data/", response_model=List[Any])
def insert_from_xlsx(*,
                     db: Session = Depends(deps.get_db),
                     file: UploadFile = File(...),
                     schema: str,
                     current_user: models.User = Depends(deps.get_current_active_superuser),
                     ) -> Any:
    """
    """
    name = decode_schemas(schema)
    all_data = save_data.get_data_xlsx(file.filename, "ancien_etudiant")
    return all_data


@router.post("/uploadfile/")
async def create_upload_file(*,
                             uploaded_file: UploadFile = File(...),
                             schema: str,
                             current_user: models.User = Depends(deps.get_current_active_superuser)
                             ):
    file_location = f"files/excel/uploaded/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    all_data_ = {}
    cle = ""
    all_table = check_table_info(schema)
    all_sheet = save_data.get_all_sheet(file_location)
    print(all_sheet)
    print(all_table)
    if len(all_table) != len(all_sheet):
        raise HTTPException(
            status_code=400,
            detail=f"invalide file",
        )
    test = False
    for i in all_table:
        if i not in all_sheet:
            raise HTTPException(
                status_code=400,
                detail=f"invalide file {all_sheet[i]} not found",
            )

    for table in all_table:
        if table == "unite_enseing":
            cle = "key_unique"
        elif table == "element_const":
            cle = "key_unique"
        elif table == "ancien_etudiant":
            cle = "num_carte"
        elif table == "nouveau_etudiant":
            cle = "num_carte"
        valid = save_data.validation_file(file_location, table, schema)
        if valid != "valid":
            raise HTTPException(
                status_code=400,
                detail=valid
            )
        all_data = save_data.get_data_xlsx(file_location, table)
        for data in all_data:
            if table == "nouveau_etudiant":
                data["select"] = bool(data["select"])
            elif table == "ancien_etudiant":
                if data["moyenne"] == "None":
                    data["moyenne"] = 0.0
            exist_data = crud.save.exist_data(schema, table, cle, data[cle])
            if not exist_data and data[cle] != "None":
                one_data = crud.save.insert_data(schema, table, data)
        all_data_[table] = all_data

    os.remove(file_location)
    return all_data_


@router.post("/upload_note_file/")
async def create_upload_note_file(
        *,
        db: Session = Depends(deps.get_db),
        uploaded_file: UploadFile = File(...),
        schema: str,
        uuid_parcours: str,
        session: str,
        current_user: models.User = Depends(deps.get_current_active_superuser)
):
    file_location = f"files/excel/uploaded/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    all_data_ = {}
    cle = "num_carte"
    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    all_table = check_table_note(schema)
    if not parcours:
        raise HTTPException(
            status_code=400,
            detail="parcours not found"
        )
    all_semestre = parcours.semestre
    all_sheet = save_data.get_all_sheet(file_location)
    for i in range(len(all_semestre)):
        if str(all_semestre[i]) != str(all_sheet[i]):
            raise HTTPException(
                status_code=400,
                detail=f"invalide file {all_sheet[i]} not found",
            )

    for sems in all_semestre:
        for table in all_table:
            if f"note_{(parcours.abreviation).lower()}_{sems.lower()}_{session.lower()}" == table:
                print(f"note_{(parcours.abreviation).lower()}_{sems.lower()}_{session.lower()}")
                valid = save_data.validation_file_note(file_location, sems, table, schema)
                if valid != "valid":
                    raise HTTPException(
                        status_code=400,
                        detail=valid
                    )
                all_data = save_data.get_data_xlsx_note(file_location, sems)
                print(all_data)
                for data in all_data:
                    exist_data = crud.save.exist_data(schema, table, cle, data[cle])
                    if not exist_data:
                        one_data = crud.save.insert_data(schema, table, data)
                all_data_[table] = all_data

    os.remove(file_location)
    return all_data_


@router.get("/save_data/")
def save_data_to_excel(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    """
    anne_univ = crud.anne_univ.get_actual_value(db=db)
    all_table = check_table_info(create_anne(anne_univ.title))
    save_data.create_workbook(anne_univ.title, all_table, "data")
    for table in all_table:
        colums = check_columns_exist(create_anne(anne_univ.title), table)
        save_data.write_data_title(anne_univ.title, table, colums, "data")
        all_data = crud.save.read_all_data(create_anne(anne_univ.title), table)
        if all_data:
            save_data.insert_data_xlsx(anne_univ.title, table, all_data, colums, "data")

    all_table = check_table_info("public")
    save_data.create_workbook("public", all_table, "data")
    for table in all_table:
        colums = check_columns_exist("public", table)
        save_data.write_data_title("public", table, colums, "data")
        all_data = crud.save.read_all_data("public", table)
        if all_data:
            save_data.insert_data_xlsx("public", table, all_data, colums, "data")
    return {"msg": "succes"}
