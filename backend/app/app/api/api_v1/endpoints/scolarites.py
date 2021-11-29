from app import crud
from app.utils import get_niveau, decode_schemas, creaate_registre
from fastapi import APIRouter, Depends, File
from sqlalchemy.orm import Session
from app import models
from typing import Any
from app.api import deps
from fastapi.responses import FileResponse
from datetime import date
import locale, time
from app.utils_sco.scolarite import create_certificat_scolarite

router = APIRouter()

@router.get("/certificat")
def certificat(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    etudiant = crud.ancien_etudiant.get_by_num_carte(schema,num_carte)
    parcours = crud.parcours.get_by_uuid(db=db,uuid=etudiant.uuid_parcours)
    mention = crud.mention.get_by_uuid(db=db,uuid=etudiant.uuid_mention)
    data = {}
    data['nom']=etudiant.nom
    data['prenom']=etudiant.prenom
    data['date_naiss']=etudiant.date_naiss
    data['lieu_naiss']=etudiant.lieu_naiss
    data['niveau']=get_niveau(etudiant.semestre_petit,etudiant.semestre_grand)
    data['mention']=mention.title
    data['parcours']=parcours.title
    data['registre']=creaate_registre(schema)
    date_ = date.today()
    anne = decode_schemas(schema)
    file = create_certificat_scolarite(num_carte,date_.year, anne, data)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)


@router.get("/relever")
def relever(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    schemas: str,
    semestre: str,
    parcours:str,
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    note = {}
    et_un_final = crud.note.read_by_num_carte(schemas, semestre, parcours,"final",num_carte)
    print(et_un_final)

