from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud
from app import models, schemas
from app.api import deps
from app.utils import decode_schemas, get_niveau, find_in_list
from app.utils_sco import carte_avant, arrire_carte

router = APIRouter()


@router.get("/carte_student/")
def create_carte(
        college_year: str,
        id_mention: str,
        id_journey: str = "",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """
    students = crud.ancien_student.get_by_mention(db=db, id_mention=id_mention,skip=0, limit=1000,
                                                  order_by="num_carte", id_journey=id_journey, year=college_year)

    mention = crud.mention.get_by_id(db=db, uuid=id_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    year = crud.college_year.get_by_title(db=db, title=college_year)
    if not year:
        raise HTTPException(status_code=400, detail=f"College years not found.", )

    all_student = []
    for on_student in students:
        if on_student.num_carte and find_in_list(on_student.actual_years, college_year) != -1:
            stud = jsonable_encoder(on_student)
            stud['level'] = get_niveau(on_student.inf_semester, on_student.sup_semester)
            stud['sex'] = on_student.sex
            stud['journey'] = crud.journey.get_by_id(db=db, uuid=on_student.id_journey).abbreviation
            all_student.append(stud)

    role = crud.role.get_title(db=db, title="chefsco")
    data = {'supperadmin': ""}

    chefsco: schemas.User = Any
    if role:
        chefsco = crud.user.get_chefsco(db=db, id_role=role.id)
        data['supperadmin'] = f"{chefsco.last_name} {chefsco.first_name}"
    data['mention'] = mention.title
    data['key'] = year.code
    data['img_carte'] = (mention.plugged.lower())[0:1]

    file = carte_avant.PDF.parcourir_et(all_student, data)

    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/carte_after/")
def create_after_carte(
        college_year: str,
        id_mention: str,
        id_journey: str = "",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """
    year = crud.college_year.get_by_title(db=db, title=college_year)
    if not year:
        raise HTTPException(status_code=400, detail=f"College year not found.",
                            )
    students = crud.ancien_student.get_by_mention(db=db, id_mention=id_mention,skip=0, limit=1000,
                                                  order_by="num_carte", id_journey=id_journey, year=college_year)

    mention = crud.mention.get_by_id(db=db, uuid=id_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    all_student = []
    for on_student in students:
        if on_student.num_carte and find_in_list(on_student.actual_years, college_year) != -1:
            stud = jsonable_encoder(on_student)
            stud['level'] = get_niveau(on_student.inf_semester, on_student.sup_semester)
            stud['journey'] = crud.journey.get_by_id(db=db, uuid=on_student.id_journey).abbreviation
            all_student.append(stud)

    role = crud.role.get_title(db=db, title="chefsco")
    data = {'supperadmin': ""}

    if role:
        chefsco = crud.user.get_chefsco(db=db, id_role=role.id)
        data['supperadmin'] = f"{chefsco.first_name} {chefsco.last_name}"

    data['mention'] = mention.title
    data['key'] = year.code
    data['img_carte'] = (mention.plugged.lower())[0:1]

    file = arrire_carte.PDF.parcourir_et(all_student, data)

    return FileResponse(path=file, media_type='application/octet-stream', filename=file)