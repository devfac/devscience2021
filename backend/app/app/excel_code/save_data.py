from typing import Any
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
 
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
    for index, columns in enumerate(columns):
        sheet.cell(row=1,column=index+1).value = columns
    
    wb.save(filename = f'files/excel/{type}/{name}.xlsx')


def insert_data_xlsx(name:str,sheet_name:str, all_data:Any, columns:list, type:str):
    wb = load_workbook(f'files/excel/{type}/{name}.xlsx')
    sheet = wb.get_sheet_by_name(sheet_name)
    row =2
    for index_, data in enumerate(all_data):
        for index,col in enumerate(data):
            sheet.cell(row=row,column=index+1).value = str(data[index])
            print(f"{sheet_name}",data[index])
        row += 1
    
    wb.save(filename = f'files/excel/{type}/{name}.xlsx')

def insert_from_xlsx(name:str,sheet_name:str, all_data:Any, columns:list, type:str):
    wb = load_workbook(f'files/excel/{type}/{name}.xlsx')
    sheet = wb.get_sheet_by_name(sheet_name)
    row =2
    for index_, data in enumerate(all_data):
        for index,col in enumerate(data):
            sheet.cell(row=row,column=index+1).value = str(data[index])
            print(f"{sheet_name}",data[index])
        row += 1
    
    wb.save(filename = f'files/excel/{type}/{name}.xlsx')