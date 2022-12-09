from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import models
from app.api import deps
from fastapi.responses import FileResponse
from app.statistic import all_statistic, stat_by_nation, stat_diplome, stat_renseignement, bachelier
from app import crud
from app.utils import decode_schemas, get_max, find_in_list
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/all_statistic/")
def all_statistic_(
        college_year: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    all_statistic
    """
    college_years = crud.college_year.get_by_title(db=db, title=college_year)
    if not college_years:
        raise HTTPException(status_code=400, detail=f"{college_year} not found.", )

    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    all_journey = crud.journey.get_by_mention(db=db, uuid_mention=uuid_mention)

    level_ = ["L1", "L2", "L3", "M1", "M2"]
    all_level = [{"L1": ["S1", "S2"]}, {"L2": ["S3", "S4"]}, {"L3": ["S5", "S6"]}, {"M1": ["S7", "S8"]},
                  {"M2": ["S9", "S10"]}]
    all_level_stat = [{"L1": []}, {"L2": []}, {"L3": []}, {"M1": []}, {"M2": []}]

    for index, level in enumerate(all_level):
        for journey in all_journey:
            if level[level_[index]][0] in journey.semester or level[level_[index]][1] in journey.semester:
                info = {"name": journey.abbreviation.upper(), "uuid": journey.uuid}
                all_level_stat[index][level_[index]].append(info)
    all_level_stat.append(
        {"H": [{"name": "6 eme", "uuid": ""}, {"name": "7 eme", "uuid": ""}, {"name": "Doctorat", "uuid": ""}]})
    data = {"anne": college_year, "mention": mention.title}
    file = all_statistic.PDF.create_all_statistic(db, data, all_level_stat, college_year)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/statistic_by_years/")
def statistic_by_years(
        college_year: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    statistic_by_years
    """
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    all_journey = crud.journey.get_by_mention(db=db, uuid_mention=uuid_mention)

    niveau_ = ["L1", "L2", "L3", "M1", "M2"]
    all_niveau = [{"L1": ["S1", "S2"]}, {"L2": ["S3", "S4"]}, {"L3": ["S5", "S6"]}, {"M1": ["S7", "S8"]},
                  {"M2": ["S9", "S10"]}]
    all_niveau_stat = [{"L1": []}, {"L2": []}, {"L3": []}, {"M1": []}, {"M2": []}]

    for index, niveau in enumerate(all_niveau):
        for journey in all_journey:
            if niveau[niveau_[index]][0] in journey.semester or niveau[niveau_[index]][1] in journey.semester:
                info = {"name": journey.abbreviation.upper()}
                etudiants = crud.ancien_student.get_by_journey_for_stat(college_year=college_year, uuid_journey=str(journey.uuid),
                                                                          semester=niveau[niveau_[index]][1])
                info["etudiants"] = etudiants
                all_niveau_stat[index][niveau_[index]].append(info)
    data = {"anne": college_year, "mention": mention.title}
    file = all_statistic.PDF.create_statistic_by_years(data, all_niveau_stat, college_year)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/statistic_by_nation/")
def statistic_by_nation(
        college_year: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    statistic_by_years
    """
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    niveau_ = ["L1", "L2", "L3", "M1", "M2"]
    all_niveau = [{"L1": "S2"}, {"L2": "S4"}, {"L3": "S6"}, {"M1": "S8"}, {"M2": "S10"}]
    all_niveau_stat = {}

    for index, niveau in enumerate(all_niveau):
        etudiants = crud.ancien_student.get_by_mention_and_niveau(college_year, str(uuid_mention), niveau[niveau_[index]])
        all_niveau_stat[niveau_[index]] = etudiants
    data = {"anne":college_year, "mention": mention.title}
    file = stat_by_nation.PDF.create_statistic_by_nation(data, all_niveau_stat, college_year)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/statistic_by_diplome/")
def statistic_by_diplome(
        schemas: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    statistic_by_years
    """
    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    etudiants_num = crud.diploma.get_by_mention(schemas, str(uuid_mention))
    etudiants = []
    for num in etudiants_num:
        un_et = {}
        un_etudiant = crud.ancien_etudiant.get_by_num_carte(schemas, num.num_carte)
        un_et["diplome"] = num.diplome
        un_et["info"] = un_etudiant
        etudiants.append(un_et)
    data = {"anne": decode_schemas(schemas), "mention": mention.title}
    file = stat_diplome.PDF.create_statistic_by_diplome(data, etudiants, schemas)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/renseignement/")
def renseignement(
        schemas: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    statistic_by_years
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schemas))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.", )

    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )
    niveau = ["L1", "M1", "M2"]
    etudiants = crud.nouveau_etudiant.get_by_mention(schemas, str(uuid_mention))
    info = {}
    for niv in niveau:
        all_etudiants = []
        for un_etudiant in etudiants:
            if un_etudiant.niveau == niv:
                all_etudiants.append(un_etudiant)
        info[niv] = all_etudiants
    data = {"annee": decode_schemas(schemas), "mention": mention.title}
    file = stat_renseignement.create_stat_renseignement(data, info, db, uuid_mention)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/bachelier/")
def bachelier_(
        schemas: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    statistic_by_years
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schemas))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.", )

    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )
    niveau = ["L1"]
    etudiants = crud.new_student.get_by_mention(schemas, str(uuid_mention))
    info = {}
    for niv in niveau:
        all_etudiants = []
        for un_etudiant in etudiants:
            if un_etudiant.niveau == niv:
                all_etudiants.append(un_etudiant)
        info[niv] = all_etudiants
    data = {"annee": decode_schemas(schemas), "mention": mention.title}
    file = bachelier.PDF.create_stat_bachelier(data, info, schemas, db, uuid_mention)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)

@router.get("/dashboard")
def dashboard(
        college_year: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> dict:
    """
    Dashboard
    """
    l1 = 0; l2=0; l3=0; m=0; pl=0; rl=0; tl=0; pm=0; rm=0; tm=0;
    mention_list:list[str]= current_user.uuid_mention
    for uuid_mention in mention_list:
        mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
        if mention:
            students = crud.ancien_student.get_by_mention(db=db, uuid_mention=uuid_mention, skip=0,
                                                          limit=1000)
            for student in students:
                semester: str = get_max(student.inf_semester, student.sup_semester)
                if find_in_list(student.actual_years, college_year) != -1:
                    if semester == "S2" or semester == "S1":
                        l1 += 1
                        if student.type == "Passant":
                            pl += 1
                        elif student.type == "Redoublant":
                            rl += 1
                        elif student.type == "Triplant ou plus":
                            tl += 1
                    elif semester == "S3" or semester == "S4":
                        l2 += 1
                        if student.type == "Passant":
                            pl += 1
                        elif student.type == "Redoublant":
                            rl += 1
                        elif student.type == "Triplant ou plus":
                            tl += 1
                    elif semester == "S5" or semester == "S6":
                        l3 += 1
                        if student.type == "Passant":
                            pl += 1
                        elif student.type == "Redoublant":
                            rl += 1
                        elif student.type == "Triplant ou plus":
                            tl += 1
                    elif semester == "S7" or semester == "S8":
                        m += 1
                        if student.type == "Passant":
                            pm += 1
                        elif student.type == "Redoublant":
                            rm += 1
                        elif student.type == "Triplant ou plus":
                            tm += 1
                    elif semester == "S9" or semester == "S10":
                        m += 1
                        if student.type == "Passant":
                            pm += 1
                        elif student.type == "Redoublant":
                            rm += 1
                        elif student.type == "Triplant ou plus":
                            tm += 1
    value: dict = {"L1":l1, "L2":l2, "L3":l3, "M":m, "PL":pl, "RL":rl, "TL":tl, "PM":pm, "RM":rm, "TM":tm}
    return value
