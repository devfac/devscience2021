import json
import os
from os import getcwd
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas, utils
from app.api import deps
from app.utils import create_num_carte, find_in_list

router = APIRouter()


@router.get("/ancien/", response_model=schemas.ResponseData)
def read_ancien_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_mention: str,
        uuid_journey: str = "",
        semester: str = "",
        limit: int = 100,
        offset: int = 0,
        order: str = "asc",
        order_by: str = "last_name",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve ancien student.
    """
    students = crud.ancien_student.get_by_mention(db=db, order_by=order_by, order=order, uuid_journey=uuid_journey,
                                                  semester=semester, uuid_mention=uuid_mention,
                                                  limit=limit, skip=offset, year=college_year)
    all_student = []
    count = 0
    for student in crud.ancien_student.count_by_mention(db=db, uuid_mention=uuid_mention, uuid_journey=uuid_journey,
                                                        semester=semester):
        if find_in_list(current_user.uuid_mention, str(student.uuid_mention)) != -1 and student.uuid_journey:
            count += 1
    for on_student in students:
        print(on_student.actual_years, on_student.num_carte)
        if on_student.uuid_journey:
            for receipt in on_student.receipt_list:
                receipt = receipt.replace("'",'"')
                receipt = json.loads(receipt)
                if receipt['year'] == college_year:
                    on_student.receipt = receipt
                    break
            stud = schemas.AncienStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            if find_in_list(current_user.uuid_mention, str(stud.uuid_mention)) != -1:
                all_student.append(stud)
    response = schemas.ResponseData(**{'count': count, 'data': all_student})
    return response


@router.get("/new/all/", response_model=schemas.ResponseData)
def read_new_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_mention: str,
        limit: int = 100,
        offset: int = 0,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve new student.
    """
    students = crud.new_student.get_by_mention(db=db,uuid_mention=uuid_mention,
                                               college_year=college_year, limit=limit, skip=offset)
    all_student = []
    count = len(crud.new_student.count_by_mention(db=db, uuid_mention=uuid_mention,  college_year=college_year))
    for on_student in students:
        on_student.mention = crud.mention.get_by_uuid(db=db, uuid=on_student.uuid_mention)
        if find_in_list(current_user.uuid_mention, str(on_student.uuid_mention)) != -1 and\
                find_in_list(on_student.actual_years, college_year) != -1:
            all_student.append(on_student)
    response = schemas.ResponseData(**{'count': count, 'data': all_student})
    return response

@router.get("/new_inscrit/", response_model=schemas.ResponseData)
def read_new_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_mention: str,
        level: str = '',
        limit: int = 100,
        offset: int = 0,
        order: str = "asc",
        order_by: str = "last_name",
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve new student.
    """
    students = crud.new_student.get_by_mention(db=db,uuid_mention=uuid_mention,college_year=college_year, level=level,
                                               order_by=order_by, order=order, limit=limit, skip=offset)
    all_student = []
    count = 0
    for student in crud.new_student.count_by_mention(db=db, uuid_mention=uuid_mention, college_year=college_year, level=level):
        if find_in_list(current_user.uuid_mention, str(student.uuid_mention)) != -1 and \
                find_in_list(student.actual_years, college_year) != -1 and student.uuid_journey:
            count += 1
    for on_student in students:
        if on_student.uuid_journey:
            for receipt in on_student.receipt_list:
                receipt = receipt.replace("'",'"')
                receipt = json.loads(receipt)
                if receipt['year'] == college_year:
                    on_student.receipt = receipt
                    break
            stud = schemas.NewStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            stud.mention = crud.mention.get_by_uuid(db=db, uuid=on_student.uuid_mention)
            if find_in_list(current_user.uuid_mention, str(on_student.uuid_mention)) != -1 and \
                    find_in_list(stud.actual_years, college_year) != -1:
                all_student.append(stud)
    response = schemas.ResponseData(**{'count': count, 'data': all_student})
    return response

@router.post("/ancien/", response_model=schemas.AncienStudent)
def create_ancien_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
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
        student_in.actual_years = [str(college_year)]
        student = crud.ancien_student.create(db=db, obj_in=student_in)
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
        if find_in_list(student.actual_years, college_year) == -1:
            actual_year:List[str] = student.actual_years if student.actual_years else []
            new_year = [str(college_year)]
            for year in actual_year:
                new_year.append(str(year))
            student_in.actual_years = new_year
        else:
            student_in.actual_years = student.actual_years
        student = crud.ancien_student.update(db=db, db_obj=student, obj_in=student_in)
    return student

@router.post("/list/", response_model=List[schemas.NewStudent])
def create_new_student(
        *,
        db: Session = Depends(deps.get_db),
        uuid_mention: str,
        uuid_journey: str,
        college_year: str,
        students: List[schemas.NewStudentUploaded],
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new student.
    """
    all_student = []
    for student_in in students:
        student_in.uuid_mention = uuid_mention
        student_in.uuid_journey = uuid_journey
        student_in.actual_years = [college_year]
        student_in.receipt_list = []
        student = crud.new_student.create(db=db, obj_in=student_in)
        all_student.append(student)
    return all_student

@router.post("/new/", response_model=schemas.SelectStudentBase)
def create_new_student(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
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
            student_in.actual_years = [college_year]
            student = crud.new_student.create(db=db, obj_in=student_in)
        else:
            raise HTTPException(status_code=404, detail="Number already exist")
    else:
        if find_in_list(student.actual_years, college_year) == -1:
            student_in.actual_years = student.actual_years.append(college_year)
        student = crud.new_student.update(db=db, db_obj=student, obj_in=student_in)
    return student

@router.put("/update_photo/",  response_model=schemas.NewStudent)
def update_student_selected(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.StudentUpdatePhoto,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
):
    one_student = crud.ancien_student.get_by_num_carte(db=db, num_carte=num_carte)
    if one_student:
        print(one_student, student_in)
        return crud.new_student.update(db=db, db_obj=one_student, obj_in=student_in)
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@router.put("/new/",  response_model=schemas.NewStudent)
def update_student_selected(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.NewStudentUpdate,
        num_select: str,
        college_year: str,
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

    students = crud.new_student.get_student_admis(db=db, college_year=college_year,
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

    student_in.receipt = ""
    if student.num_carte:
        student_in.num_carte = student.num_carte
    else:
        student_in.num_carte = create_num_carte(mention.plugged, str(num))

    student_in.inf_semester = utils.get_sems_min(student.level)
    student_in.sup_semester = utils.get_sems_max(student.level)
    student = crud.new_student.update(db=db, db_obj=student, obj_in=student_in)
    return student


@router.get("/num_carte/", response_model=schemas.AncienStudent)
def read_student_by_num_carte(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        college_year: str,
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
            if receipt['year'] == college_year:
                stud.receipt = receipt
        if find_in_list(current_user.uuid_mention, str(stud.uuid_mention)) != -1:
            return stud


@router.get("/new_selected/", response_model=schemas.NewStudent)
def read_student_by_num_select(
        *,
        db: Session = Depends(deps.get_db),
        num_select: str,
        college_year: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by num select.
    """
    student = crud.new_student.get_by_num_select(db=db, num_select=num_select)
    if not student or not find_in_list(current_user.uuid_mention, str(student.uuid_mention)) != -1:
        raise HTTPException(status_code=404, detail="Student not found")

    if not student.is_selected:
        raise HTTPException(status_code=404, detail="Student not selected")

    if student.uuid_journey:
        stud = schemas.NewStudent(**jsonable_encoder(student))
        stud.journey = crud.journey.get_by_uuid(db=db, uuid=student.uuid_journey)
        for receipt in student.receipt_list:
            receipt = receipt.replace("'", '"')
            receipt = json.loads(receipt)
            if receipt['year'] == college_year:
                stud.receipt = receipt
        if find_in_list(current_user.uuid_mention, str(stud.uuid_mention)) != -1:
            return stud
    return student

@router.get("/new_num_carte/", response_model=schemas.NewStudent)
def read_student_by_num_carte(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        college_year: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by num select.
    """
    student = crud.new_student.get_by_num_carte(db=db, num_carte=num_carte)
    if not student or not find_in_list(current_user.uuid_mention, str(student.uuid_mention)) != -1:
        raise HTTPException(status_code=404, detail="Student not found")

    if not student.is_selected:
        raise HTTPException(status_code=404, detail="Student not selected")

    if student.receipt_list:
        for receipt in student.receipt_list:
            receipt = receipt.replace("'", '"')
            receipt = json.loads(receipt)
            if receipt['year'] == college_year:
                student.receipt = receipt
    return student

@router.get("/new/", response_model=schemas.NewStudent)
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


@router.get("/ancien/by_journey/", response_model=List[schemas.AncienStudent])
def read_student_by_journey(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_journey: str,
        limit: int,
        offset: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by journey.
    """
    student = crud.ancien_student.get_by_jouney(db=db, uuid_journey=uuid_journey,
                                                college_year=college_year, limit=limit, skip=offset)
    return student


@router.get("/new/by_journey/", response_model=List[schemas.NewStudent])
def read_student_by_journey(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_journey: str,
        limit: int,
        offset: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by journey.
    """
    student = crud.new_student.get_by_jouney(db=db, uuid_journey=uuid_journey,
                                             college_year=college_year, limit=limit, skip=offset)
    return student


@router.get("/ancien/by_sup_semester_and_mention/", response_model=List[schemas.AncienStudent])
def read_student_by_sup_semester_and_mention(
        *,
        db: Session = Depends(deps.get_db),
        college_year: str,
        uuid_mention: UUID,
        sup_semester: str,
        limit: int,
        offset: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by semester and mention.
    """
    students = crud.ancien_student.get_by_sup_semester_and_mention(
        db=db, uuid_mention=uuid_mention, sup_semester=sup_semester,
        college_year=college_year, limit=limit, skip=offset)
    all_student = []
    for on_student in students:
        if on_student.uuid_journey:
            stud = schemas.AncienStudent(**jsonable_encoder(on_student))
            stud.journey = crud.journey.get_by_uuid(db=db, uuid=on_student.uuid_journey)
            all_student.append(stud)
    return all_student


@router.delete("/ancien/", response_model=List[schemas.AncienStudent])
def delete_student(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
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
    return student


@router.delete("/new/", response_model=Any)
def delete_student(
        *,
        db: Session = Depends(deps.get_db),
        num_select: str,
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

    return student


@router.get("/photo/")
def get_file(name_file: str):
    path = getcwd() + "/files/photos/" + name_file
    if os.path.exists(path):
        return FileResponse(path=path)


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
