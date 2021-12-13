from typing import Any
import uuid
from openpyxl.workbook import Workbook
from openpyxl import load_workbook

from app.utils import check_columns_exist
 
def create_workbook(name:str, sheet_name:list, type:str):
    wb = Workbook()
    wbs = []
    for index, sheet in enumerate(sheet_name):
        wbs.append(sheet)
        wbs[index] = wb.create_sheet(sheet, index)
        wbs[index].title = sheet
    wb.save(filename = f'files/excel/{type}/{name}.xlsx')


def gwrite_data_title(name:str, sheet_name:str,columns:list, type:str):
    wb = load_workbook(f'files/excel/{type}/{name}.xlsx')
    sheet = wb.get_sheet_by_name(sheet_name)
    for index, colum in enumerate(columns):
        sheet.cell(row=1,column=index+1).value = colum
    
    wb.save(filename = f'files/excel/{type}/{name}.xlsx')


def insert_data_xlsx(name:str,sheet_name:str, all_data:Any, columns:list, type:str):
    wb = load_workbook(f'files/excel/{type}/{name}.xlsx')
    sheet = wb.get_sheet_by_name(sheet_name)
    row =2
    for index_, data in enumerate(all_data):
        for index,col in enumerate(data):
            sheet.cell(row=row,column=index+1).value = str(data[index])
        row += 1
    
    wb.save(filename = f'files/excel/{type}/{name}.xlsx')


def insert_from_xlsx(name:str,sheet_name:str, all_data:Any, columns:list, type:str):
    wb = load_workbook(f'files/excel/{type}/{name}.xlsx')


def get_all_sheet(workbook:str):
    wb = load_workbook(workbook)
    return wb.sheetnames


def validation_file(name:str,sheet_name:str, schemas:str)-> str:
    wb = load_workbook(name)
    sheet = wb.get_sheet_by_name(sheet_name)
    columns = check_columns_exist(schemas,sheet_name)
    for col in range(sheet.max_column):
        if str(sheet.cell(row=1,column=col+1).value) != columns[col]:
            return f"invalid columns {columns[col]} and {sheet.cell(row=1,column=col+1).value} is differents"
    return "valid"

def validation_file_note(name:str,sheet_name:str, table_name:str,schemas:str)-> str:
    wb = load_workbook(name)
    sheet = wb.get_sheet_by_name(sheet_name)
    columns = check_columns_exist(schemas,table_name)
    for col in range(sheet.max_column):
        if str(sheet.cell(row=1,column=col+1).value) != columns[col]:
            return f"invalid columns {columns[col]} and {sheet.cell(row=1,column=col+1).value} is differents"
    return "valid"


def get_data_xlsx(name:str,sheet_name:str)-> Any:
    wb = load_workbook(name)
    sheet = wb.get_sheet_by_name(sheet_name)
<<<<<<< HEAD
    row =2
    for index_, data in enumerate(all_data):
        for index,col in enumerate(data):
            sheet.cell(row=row,column=index+1).value = str(data[index])
            print(f"{sheet_name}",data[index])
        row += 1
    
    wb.save(filename = f'files/excel/{type}/{name}.xlsx')
=======
    all_data = []
    for row in range(sheet.max_row):
        data = {}
        if row != 0 :
            data['uuid']=str(uuid.uuid4())
            for col in range(sheet.max_column-1):
                data[str(sheet.cell(row=1,column=col+2).value)]= str(sheet.cell(row=row+1,column=col+2).value)
            all_data.append(data) 
    return all_data


def get_data_xlsx_note(name:str,sheet_name:str)-> Any:
    wb = load_workbook(name)
    sheet = wb.get_sheet_by_name(sheet_name)
    all_data = []
    for row in range(sheet.max_row):
        data = {}
        if row != 0 :
            for col in range(sheet.max_column):
                data[str(sheet.cell(row=1,column=col+1).value)]= str(sheet.cell(row=row+1,column=col+1).value)
            all_data.append(data) 
    return all_data
>>>>>>> excel
