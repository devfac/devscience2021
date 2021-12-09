import os
from typing import Any, List

from fastapi import APIRouter, Depends, File, UploadFile,HTTPException
from pydantic.networks import EmailStr
from sqlalchemy.sql.expression import any_
import aiofiles

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import check_table_info, create_anne,check_columns_exist, decode_schemas
from app.excel_code import save_data
from app import crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/get_models/")
def get_models(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    """
    anne_univ = crud.anne_univ.get_multi(db=db)
    for anne in anne_univ:
        all_table = check_table_info(create_anne(anne.title))
        save_data.create_workbook(anne.title,all_table,"models")
        for table in all_table:
            colums = check_columns_exist(create_anne(anne.title),table)
            save_data.write_data_title(anne.title, table,colums,"models")

    all_table = check_table_info("public")
    save_data.create_workbook("public",all_table,"models")
    for table in all_table:
            colums = check_columns_exist("public",table)
            save_data.write_data_title("public", table,colums,"models" )
    return {"msg": "Word received"}


@router.post("/insert_data/", response_model=List[Any])
def insert_from_xlsx(*,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    schema:str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    """
    name = decode_schemas(schema)
    all_data = save_data.get_data_xlsx(file.filename,"ancien_etudiant")
    return all_data


@router.post("/uploadfile/")
async def create_upload_file(*,
    uploaded_file: UploadFile = File(...),
    schema:str,
    current_user: models.User = Depends(deps.get_current_active_superuser)
    ):
    file_location = f"files/excel/uploaded/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    
    all_data_ = {}
    cle = ""
    all_table = check_table_info(schema)
    all_sheet = save_data.get_all_sheet(file_location)
    for i in range(len(all_table)):
        if str(all_table[i]) != str(all_sheet[i]):
            raise HTTPException(
            status_code=400,
            detail=f"invalide file {all_sheet[i]} not found",
        )

    for table in all_table:
        if table == "unite_enseing":
            cle = "num_carte"
        elif table == "element_const":
            cle = "num_carte"
        elif table == "ancien_etudiant":
            cle = "num_carte"
        elif table == "nouveau_etudiant":
            cle = "num_carte"
        valid = save_data.validation_file(file_location,table,schema)
        if valid != "valid":
            raise HTTPException(
            status_code=400,
            detail=f"invalide file ",
        )

        all_data = save_data.get_data_xlsx(file_location,table)
        all_data_[table]=all_data
    os.remove(file_location)
    return all_data_


@router.get("/save_data/")
def save_data_to_excel(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    """
    anne_univ = crud.anne_univ.get_multi(db=db)
    for anne in anne_univ:
        all_table = check_table_info(create_anne(anne.title))
        save_data.create_workbook(anne.title,all_table,"data")
        for table in all_table:
            colums = check_columns_exist(create_anne(anne.title),table)
            save_data.write_data_title(anne.title, table,colums,"data" )
            all_data = crud.save.read_all_data(create_anne(anne.title),table)
            if all_data:
                save_data.insert_data_xlsx(anne.title,table,all_data,colums,"data")

    all_table = check_table_info("public")
    save_data.create_workbook("public",all_table,"data")
    for table in all_table:
        colums = check_columns_exist("public",table)
        save_data.write_data_title("public", table,colums,"data" )
        all_data = crud.save.read_all_data("public",table)
        if all_data:
            save_data.insert_data_xlsx("public",table,all_data,colums,"data")
    return {"msg": "Word received"}
