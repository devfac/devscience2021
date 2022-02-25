from typing import Any

from sqlalchemy.sql.functions import percentile_cont

from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email
from fastapi.responses import FileResponse
from app.utils_sco import carte_avant, arrire_carte
from app import crud
from app.utils import decode_schemas, get_niveau
from sqlalchemy.orm import Session
import json
from app.utils import UUIDEncoder

router = APIRouter()


@router.get("/carte_etudiant/")
def create_carte(
        schema: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",
                            )
    etudiants_ = crud.ancien_etudiant.get_by_mention(schema, uuid_mention)

    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    all_etudiant = []
    if etudiants_:
        for un_etudiant in etudiants_:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et['niveau'] = get_niveau(un_etudiant.semestre_petit, un_etudiant.semestre_grand)
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abreviation
            all_etudiant.append(et)

    role = crud.role.get_title(db=db, title="chefsco")
    data = {}
    data['supperadmin'] = ""

    chefsco: schemas.User = Any
    if role:
        chefsco = crud.user.get_chefsco(db=db, uuid_role=role.uuid)
        data['supperadmin'] = f"{chefsco.first_name} {chefsco.last_name}"

    data['mention'] = mention.title
    data['key'] = anne_univ.code
    data['img_carte'] = (mention.branche.lower())[0:1]

    file = carte_avant.PDF.parcourir_et(all_etudiant, data)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/carte_etudiant_ariere/")
def create_ariere_carte(
        schema: str,
        uuid_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create liste au examen
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",
                            )
    etudiants_ = crud.ancien_etudiant.get_by_mention(schema, uuid_mention)

    mention = crud.mention.get_by_uuid(db=db, uuid=uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    all_etudiant = []
    if etudiants_:
        for un_etudiant in etudiants_:
            et = json.loads(json.dumps(dict(un_etudiant), cls=UUIDEncoder))
            et['niveau'] = get_niveau(un_etudiant.semestre_petit, un_etudiant.semestre_grand)
            et["parcours"] = crud.parcours.get_by_uuid(db=db, uuid=un_etudiant.uuid_parcours).abreviation
            all_etudiant.append(et)

    role = crud.role.get_title(db=db, title="chefsco")
    data = {}
    data['supperadmin'] = ""

    chefsco: schema.User = Any
    if role:
        chefsco = crud.user.get_chefsco(db=db, uuid_role=role.uuid)
        data['supperadmin'] = f"{chefsco.first_name} {chefsco.last_name}"

    data['mention'] = mention.title
    data['key'] = anne_univ.code
    data['img_carte'] = (mention.branche.lower())[0:1]

    file = arrire_carte.PDF.parcourir_et(all_etudiant, data)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)
