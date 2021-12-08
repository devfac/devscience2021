from typing import Any, List

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic.networks import EmailStr
from sqlalchemy.sql.expression import any_

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


@router.get("/insert_data/", response_model=List[Any])
def insert_from_xlsx(*,
    db: Session = Depends(deps.get_db),
    schema:str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    """
    name = decode_schemas(schema)
    all_data = save_data.get_data_xlsx(name,"ancien_etudiant","data")
    return all_data

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": len(file)}

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
