from app import crud
from app.utils import get_niveau, decode_schemas, creaate_registre
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from typing import Any
from app.api import deps
from fastapi.responses import FileResponse
from datetime import date
import locale, time
from app.utils_sco.scolarite import create_certificat_scolarite
from app.utils_sco.relever import PDF

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
    if etudiant:
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
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")

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
    ue = {}
    ues = []
    et_un_final = crud.note.read_by_num_carte(schemas, semestre, parcours,"final",num_carte)
    etudiant = crud.ancien_etudiant.get_by_num_carte(schemas,num_carte)
    if et_un_final and etudiant:
        matier_ues = crud.matier_ue.get_by_class(schemas,uuid_parcours,semestre)
        note['num_carte']=num_carte
        note['moyenne']=et_un_final['moyenne']
        note['credit']=et_un_final['credit']
        for  matier_ue in matier_ues:
            ue['name']= matier_ue['title']
            ue['note']= et_un_final[f"ue_{matier_ue['value']}"]
            ue['credit']= matier_ue['credit']
            matier_ecs = crud.matier_ec.get_by_value_ue(schemas,matier_ue['value'],semestre,uuid_parcours)

            ecs = []
            for matier_ec in matier_ecs:
                ec = {}
                ec['name']= matier_ec['title']
                ec['note']= et_un_final[f"ec_{matier_ec['value']}"]
                ec['poids']= matier_ec['poids']
                ecs.append(ec.copy())
            ue['ec']=ecs
            ues.append(ue.copy())
        note['ue']=ues

        parcours = crud.parcours.get_by_uuid(db=db,uuid=etudiant.uuid_parcours)
        mention = crud.mention.get_by_uuid(db=db,uuid=etudiant.uuid_mention)
        data = {}
        data['nom']=etudiant.nom
        data['prenom']=etudiant.prenom
        data['date_naiss']=etudiant.date_naiss
        data['lieu_naiss']=etudiant.lieu_naiss
        data['semestre']=semestre
        data['mention']=mention.title
        data['parcours']=parcours.title
        data['session']="Normal"
        date_ = date.today()
        anne = decode_schemas(schemas)
        file = PDF.relever_note(num_carte,date_.year, anne, data,note)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")

