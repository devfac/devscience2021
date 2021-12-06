from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import check_table_info, create_anne,check_columns_exist
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
            all_data = crud.save.read_all_data(create_anne(anne.title),table)
            if all_data:
                save_data.insert_data_xlsx(anne.title,table,all_data,colums,"data")
    all_table = check_table_info("public")
    save_data.create_workbook("public",all_table,"models")
    for table in all_table:
            colums = check_columns_exist("public",table)
            save_data.write_data_title("public", table,colums,"models" )
    return {"msg": "Word received"}


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
            schemas = create_anne(anne.title)

    all_table = check_table_info("public")
    save_data.create_workbook("public",all_table,"data")
    for table in all_table:
            colums = check_columns_exist("public",table)
            save_data.write_data_title("public", table,colums,"data" )
    return {"msg": "Word received"}
