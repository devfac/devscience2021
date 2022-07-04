from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import models
from app.api import deps
from fastapi.responses import FileResponse
from app.statistic import all_statistic, stat_by_nation, stat_diplome, stat_renseignement, bachelier
from app import crud
from app.utils import decode_schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/all_statistic/")
def all_statistic_(
        schemas: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    all_statistic
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schemas))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.", )

    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    all_parcours = crud.parcours.get_by_mention(db=db, uuid_mention=uuid_mention)

    niveau_ = ["L1", "L2", "L3", "M1", "M2"]
    all_niveau = [{"L1": ["S1", "S2"]}, {"L2": ["S3", "S4"]}, {"L3": ["S5", "S6"]}, {"M1": ["S7", "S8"]},
                  {"M2": ["S9", "S10"]}]
    all_niveau_stat = [{"L1": []}, {"L2": []}, {"L3": []}, {"M1": []}, {"M2": []}]

    for index, niveau in enumerate(all_niveau):
        for parcours in all_parcours:
            if niveau[niveau_[index]][0] in parcours.semestre or niveau[niveau_[index]][1] in parcours.semestre:
                info = {"name": parcours.abbreviation.upper(), "uuid": parcours.uuid}
                all_niveau_stat[index][niveau_[index]].append(info)
    all_niveau_stat.append(
        {"H": [{"name": "6 eme", "uuid": ""}, {"name": "7 eme", "uuid": ""}, {"name": "Doctorat", "uuid": ""}]})
    data = {"anne": decode_schemas(schemas), "mention": mention.title}
    file = all_statistic.PDF.create_all_statistic(data, all_niveau_stat, schemas)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/statistic_by_years/")
def statistic_by_years(
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

    all_parcours = crud.parcours.get_by_mention(db=db, uuid_mention=uuid_mention)

    niveau_ = ["L1", "L2", "L3", "M1", "M2"]
    all_niveau = [{"L1": ["S1", "S2"]}, {"L2": ["S3", "S4"]}, {"L3": ["S5", "S6"]}, {"M1": ["S7", "S8"]},
                  {"M2": ["S9", "S10"]}]
    all_niveau_stat = [{"L1": []}, {"L2": []}, {"L3": []}, {"M1": []}, {"M2": []}]

    for index, niveau in enumerate(all_niveau):
        for parcours in all_parcours:
            if niveau[niveau_[index]][0] in parcours.semestre or niveau[niveau_[index]][1] in parcours.semestre:
                info = {"name": parcours.abbreviation.upper()}
                etudiants = crud.ancien_etudiant.get_by_parcours_for_stat(schemas, str(parcours.uuid),
                                                                          niveau[niveau_[index]][1])
                info["etudiants"] = etudiants
                all_niveau_stat[index][niveau_[index]].append(info)
    data = {"anne": decode_schemas(schemas), "mention": mention.title}
    file = all_statistic.PDF.create_statistic_by_years(data, all_niveau_stat, schemas)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/statistic_by_nation/")
def statistic_by_nation(
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

    niveau_ = ["L1", "L2", "L3", "M1", "M2"]
    all_niveau = [{"L1": "S2"}, {"L2": "S4"}, {"L3": "S6"}, {"M1": "S8"}, {"M2": "S10"}]
    all_niveau_stat = {}

    for index, niveau in enumerate(all_niveau):
        etudiants = crud.ancien_etudiant.get_by_mention_and_niveau(schemas, str(uuid_mention), niveau[niveau_[index]])
        all_niveau_stat[niveau_[index]] = etudiants
    data = {"anne": decode_schemas(schemas), "mention": mention.title}
    file = stat_by_nation.PDF.create_statistic_by_nation(data, all_niveau_stat, schemas)
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
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schemas))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.", )

    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    etudiants_num = crud.diplome.get_by_mention(schemas, str(uuid_mention))
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
    etudiants = crud.nouveau_etudiant.get_by_mention(schemas, str(uuid_mention))
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
