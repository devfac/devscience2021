import json
import os
from os import getcwd
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.schemas.student import Receipt
from app.utils import create_num_carte, find_in_list
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/ancien", response_model=List[schemas.AncienStudent])
def read_ancien_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_mention: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve ancien student.
    """
    students = crud.ancien_student.get_by_mention(db=db, college_year=college_year, uuid_mention=uuid_mention)
    all_student = []
    for on_student in students:
        if on_student.uuid_journey:
            for receipt in on_student.receipt_list:
                receipt = receipt.replace("'",'"')
                receipt = json.loads(receipt)
                if receipt['year'] == on_student.actual_years:
                    on_student.receipt = receipt
                    break
            stud = schemas.AncienStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            if find_in_list(current_user.uuid_mention, str(stud.uuid_mention)) != -1:
                all_student.append(stud)
    return all_student


@router.get("/new/all", response_model=List[schemas.SelectStudentBase])
def read_new_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_mention: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve new student.
    """
    students = crud.new_student.get_by_mention(db=db,uuid_mention=uuid_mention, college_year=college_year)
    all_student = []
    for on_student in students:
        on_student.mention = crud.mention.get_by_uuid(db=db, uuid=on_student.uuid_mention)
        if find_in_list(current_user.uuid_mention, str(on_student.uuid_mention)) != -1:
            all_student.append(on_student)
    return all_student

@router.get("/new_inscrit", response_model=List[schemas.NewStudent])
def read_new_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_mention: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve new student.
    """
    students = crud.new_student.get_by_mention(db=db,uuid_mention=uuid_mention, college_year=college_year)
    all_student = []
    for on_student in students:
        if on_student.uuid_journey:
            for receipt in on_student.receipt_list:
                receipt = receipt.replace("'",'"')
                receipt = json.loads(receipt)
                if receipt['year'] == on_student.actual_years:
                    on_student.receipt = receipt
                    break
            stud = schemas.NewStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            on_student.mention = crud.mention.get_by_uuid(db=db, uuid=on_student.uuid_mention)
            if find_in_list(current_user.uuid_mention, str(on_student.uuid_mention)) != -1:
                all_student.append(on_student)
    return all_student

@router.post("/ancien", response_model=List[schemas.AncienStudent])
def create_ancien_student(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.AncienStudentCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new student.
    """
    journey = crud.journey.get_by_uuid(db=db, uuid=student_in.uuid_journey)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")
    mention = crud.mention.get_by_uuid(db=db, uuid=student_in.uuid_mention)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")
    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=student_in.num_carte)
    if not student:
        list_receipt = [str(dict(student_in.receipt))]
        student_in.receipt_list = list_receipt
        student_in.receipt = ""
        crud.ancien_student.create(db=db, obj_in=student_in)
    else:
        k: int = 0
        list_receipt = []
        list_receipt_2 = []
        for receipt in student.receipt_list:
            receipt = receipt.replace("'",'"')
            list_receipt.append(json.loads(receipt))
        for receipt in list_receipt:
            if receipt['year'] == student_in.receipt.year:
                k = 1
                list_receipt_2.append(str(dict(student_in.receipt)))
            else:
                list_receipt_2.append(str(dict(receipt)))
        if k == 0:
            list_receipt_2.append(str(dict(student_in.receipt)))
        student_in.receipt_list = list_receipt_2
        student_in.receipt = ""
        crud.ancien_student.update(db=db, db_obj=student, obj_in=student_in)
    students = crud.ancien_student.get_all(db=db, college_year=student_in.actual_years)
    all_student = []
    for on_student in students:
        if on_student.uuid_journey:
            stud = schemas.AncienStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            for receipt in on_student.receipt_list:
                receipt = receipt.replace("'",'"')
                receipt = json.loads(receipt)
                if receipt['year'] == stud.actual_years:
                    stud.receipt = receipt
                    break
            if find_in_list(current_user.uuid_mention, str(stud.uuid_mention)) != -1:
                all_student.append(stud)
    return all_student


@router.post("/new", response_model=List[schemas.SelectStudentBase])
def create_new_student(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.SelectStudentCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new student.
    """

    mention = crud.mention.get_by_uuid(db=db, uuid=student_in.uuid_mention)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")

    student = crud.new_student.get_by_num_select(db=db, num_select=student_in.num_select)
    if not student:
        student_in.num_select = f"S{mention.abbreviation.upper()}{student_in.num_select}-{student_in.enter_years[2:4]}"
        student = crud.new_student.get_by_num_select(db=db, num_select=student_in.num_select)
        if not student:
            crud.new_student.create(db=db, obj_in=student_in)
        else:
            raise HTTPException(status_code=404, detail="Number already exist")
    else:
        crud.new_student.update(db=db, db_obj=student, obj_in=student_in)
    students = crud.new_student.get_all(db=db, college_year=student_in.actual_years)
    all_student = []
    for on_student in students:
        on_student.mention = crud.mention.get_by_uuid(db=db, uuid=on_student.uuid_mention)
        if find_in_list(current_user.uuid_mention, str(on_student.uuid_mention)) != -1:
            all_student.append(on_student)

    return all_student


@router.put("/new", response_model=List[schemas.NewStudent])
def update_student_selected(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.NewStudentUpdate,
        num_select: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new student.
    """

    journey = crud.journey.get_by_uuid(db=db, uuid=student_in.uuid_journey)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    mention = crud.mention.get_by_uuid(db=db, uuid=student_in.uuid_mention)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")

    students = crud.new_student.get_student_admis(db=db, college_year=student_in.actual_years,
                                                  uuid_mention=mention.uuid)
    all_students = []
    for student in students:
        if student.num_carte:
            all_students.append(student)
    num = int(mention.last_num_carte) + len(all_students) + 1

    student = crud.new_student.get_by_num_select(db=db, num_select=num_select)

    if not student.receipt_list:
        list_receipt = [str(dict(student_in.receipt))]
        student_in.receipt_list = list_receipt
    else:
        k: int = 0
        list_receipt = []
        list_receipt_2 = []
        for receipt in student.receipt_list:
            receipt = receipt.replace("'",'"')
            list_receipt.append(json.loads(receipt))
        for receipt in list_receipt:
            if receipt['year'] == student_in.receipt.year:
                k = 1
                list_receipt_2.append(str(dict(student_in.receipt)))
            else:
                list_receipt_2.append(str(dict(receipt)))
        if k == 0:
            list_receipt_2.append(str(dict(student_in.receipt)))
        student_in.receipt_list = list_receipt_2

    if not student or not student.is_selected:
        raise HTTPException(status_code=404, detail="Student not selected or not found")

    if student.num_carte:
        student_in.num_carte = student.num_carte
    else:
        student_in.num_carte = create_num_carte(mention.plugged, str(num))

    crud.new_student.update(db=db, db_obj=student, obj_in=student_in)
    students = crud.new_student.get_all(db=db, college_year=student_in.actual_years)
    all_student = []
    for on_student in students:
        if on_student.uuid_journey:
            stud = schemas.NewStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            if find_in_list(current_user.uuid_mention, str(stud.uuid_mention)) != -1:
                all_student.append(stud)
    return all_student


@router.get("/num_carte", response_model=schemas.AncienStudent)
def read_student_by_num_carte(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by num carte.
    """
    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.uuid_journey:
        stud = schemas.AncienStudent(**jsonable_encoder(student))
        stud.journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey)
        for receipt in student.receipt_list:
            receipt = receipt.replace("'", '"')
            receipt = json.loads(receipt)
            if receipt['year'] == student.actual_years:
                print(receipt)
                stud.receipt = receipt
        if find_in_list(current_user.uuid_mention, str(stud.uuid_mention)) != -1:
            return stud


@router.get("/new", response_model=schemas.NewStudent)
def read_student_by_num_select(
        *,
        db: Session = Depends(deps.get_db),
        num_select: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by num select.
    """
    student = crud.new_student.get_by_num_select(db=db, num_select=num_select)
    if not student or not find_in_list(current_user.uuid_mention, str(student.uuid_mention)) != -1:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/ancien/by_journey", response_model=List[schemas.AncienStudent])
def read_student_by_journey(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by journey.
    """
    student = crud.ancien_student.get_by_jouney(db=db, uuid_journey=uuid_journey, college_year=college_year)
    return student


@router.get("/new/by_journey", response_model=List[schemas.NewStudent])
def read_student_by_journey(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_journey: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by journey.
    """
    student = crud.new_student.get_by_jouney(db=db, uuid_journey=uuid_journey, college_year=college_year)
    return student


@router.get("/ancien/by_sup_semester_and_mention", response_model=List[schemas.AncienStudent])
def read_student_by_sup_semester_and_mention(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_mention: UUID,
        sup_semester: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by semester and mention.
    """
    students = crud.ancien_student.get_by_sup_semester_and_mention(
        db=db, uuid_mention=uuid_mention, sup_semester=sup_semester, college_year=college_year)
    all_student = []
    for on_student in students:
        if on_student.uuid_journey:
            stud = schemas.AncienStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            all_student.append(stud)
    return all_student


@router.delete("/ancien", response_model=List[schemas.AncienStudent])
def delete_student(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        college_year: str,
        uuid_mention: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an student.
    """
    student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student = crud.ancien_student.remove_carte(db=db, num_carte=num_carte)
    if student:
        print(os.path.exists(getcwd() + "/files/photos/" + student.photo))
        if os.path.exists(getcwd() + "/files/photos/" + student.photo):
            os.remove(getcwd() + "/files/photos/" + student.photo)
    students = crud.ancien_student.get_by_mention(db=db, college_year=college_year, uuid_mention=uuid_mention)
    all_student = []
    for on_student in students:
        if on_student.uuid_journey:
            for receipt in on_student.receipt_list:
                receipt = receipt.replace("'", '"')
                receipt = json.loads(receipt)
                if receipt['year'] == on_student.actual_years:
                    on_student.receipt = receipt
                    break
            stud = schemas.AncienStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            if find_in_list(current_user.uuid_mention, str(stud.uuid_mention)) != -1:
                all_student.append(stud)
    return all_student


@router.delete("/new", response_model=List[schemas.NewStudent])
def delete_student(
        *,
        db: Session = Depends(deps.get_db),
        num_select: str,
        college_year: str,
        uuid_mention: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an student.
    """
    student = crud.new_student.get_by_num_select(db=db, num_select=num_select)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student = crud.new_student.remove_select(db=db, num_select=num_select)
    if student and student.photo:
        if os.path.exists(getcwd() + "/files/photos/" + student.photo):
            os.remove(getcwd() + "/files/photos/" + student.photo)
    students = crud.new_student.get_by_mention(db=db, uuid_mention=uuid_mention, college_year=college_year)
    all_student = []
    for on_student in students:
        if find_in_list(current_user.uuid_mention, str(on_student.uuid_mention)) != -1:
            all_student.append(on_student)
    return all_student


@router.get("/photo")
def get_file(name_file: str):
    return FileResponse(path=getcwd() + "/files/photos/" + name_file)


@router.post("/upload_photo/")
async def create_upload_file(*,
                             uploaded_file: UploadFile = File(...),
                             num_carte: str,
                             current_user: models.User = Depends(deps.get_current_active_user)
                             ):
    name = list(os.path.splitext(uploaded_file.filename))[1]
    allowed_files = {".jpg", ".jpeg", ".png"}

    if name.lower() not in allowed_files:
        raise HTTPException(status_code=402, detail="invalid image")
    file_location = f"files/photos/{num_carte}{name}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"filename": f'{num_carte}{name}'}
