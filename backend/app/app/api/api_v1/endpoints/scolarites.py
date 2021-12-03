from app import crud
from app.utils import get_niveau, decode_schemas, creaate_registre, validation_semestre
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from typing import Any
from app.api import deps
from fastapi.responses import FileResponse
from datetime import date
from app.utils_sco.scolarite import create_certificat_scolarite
from app.utils_sco.relever import PDF
from app.utils_sco.inscription import attestation_inscription
from app.utils_sco.credit import attestation_validation_credit
from app.utils_sco.assiduite import create_certificat_assidute

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

@router.get("/attestation_inscription")
def attestation(
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
        file = attestation_inscription(num_carte,date_.year, anne, data)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")

@router.get("/validation_credit")
def attestation_validation(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    schema: str,
    niveau:str,
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
        file = attestation_validation_credit(num_carte,date_.year, niveau, data)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")

@router.get("/assiduite")
def certificat_assiduite(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    schema: str,
    rentrer:str,
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
        file = create_certificat_assidute(num_carte,date_.year, rentrer, data,)
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
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    note = {}
    ue = {}
    ues = []
    session = "Normal"
    anne = decode_schemas(schemas)
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours,session="rattrapage")
    test_note_final = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours,session="final")
    if test_note:
        et_un_rattrapage = crud.note.read_by_num_carte(schemas, semestre, parcours,"rattrapage",num_carte)
        if et_un_rattrapage:
            session = "Rattrapage"

    if not test_note_final:
        raise HTTPException( status_code=400, detail=f"note_{semestre}_{parcours}_final not found.",
        )
    et_un_final = crud.note.read_by_num_carte(schemas, semestre, parcours,"final",num_carte)
    
    etudiant = crud.ancien_etudiant.get_by_num_carte(schemas,num_carte)
    if et_un_final and etudiant:
        validation = crud.semetre_valide.get_by_num_carte(db=db, num_carte=num_carte)
        
        matier_ues = crud.matier_ue.get_by_class(schemas,etudiant.uuid_parcours,semestre)
        note['num_carte']=num_carte
        note['moyenne']=et_un_final['moyenne']
        note['credit']=et_un_final['credit']
        for  matier_ue in matier_ues:
            ue['name']= matier_ue['title']
            ue['note']= et_un_final[f"ue_{matier_ue['value']}"]
            ue['credit']= matier_ue['credit']
            matier_ecs = crud.matier_ec.get_by_value_ue(schemas,matier_ue['value'],semestre,etudiant.uuid_parcours)

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
        test_validation = {}
        if validation:
            test_validation = validation_semestre(validation, semestre,et_un_final['credit'],30,anne)
        else:
            test_validation['status'] = f"Étudiant(e) redoublé(e)."
            test_validation['code'] = False
            test_validation['anne'] = decode_schemas(schemas)
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
        data['session']=session
        data['validation']=test_validation['status']
        data['code']=test_validation['code']
        data['anne']=test_validation['anne']
        date_ = date.today()
        file = PDF.relever_note(num_carte,date_.year,data,note)
        return FileResponse(path=file, media_type='application/octet-stream', filename=file)
    else:
        raise HTTPException(status_code=404, detail="Etudiant not found")

