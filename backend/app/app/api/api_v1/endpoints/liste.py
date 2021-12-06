from typing import Any

from sqlalchemy.sql.functions import percentile_cont

from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email
from fastapi.responses import FileResponse
from app.liste import liste_exams, liste_inscrit
from app import crud
from app.utils import decode_schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/list_exam/")
def list_examen(
    schemas:str,
    semestre:str,
    uuid_parcours:str,
    uuid_mention:str,
    session:str,
    salle:str,
    skip=1,
    limit=21,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    create liste au examen
    """
    data = {}
    matiers = {} 
    ues = crud.matier_ue.get_by_class(schemas,uuid_parcours,semestre)
    all_ue = []
    for ue in ues:
        ues_={}
        ues_['name'] = ue['title']
        nbr = 0
        ecs = crud.matier_ec.get_by_value_ue(schemas,ue['value'],semestre,uuid_parcours)
        all_ec = []
        for ec in ecs:
            ecs_={}
            nbr +=1;
            ecs_['name']=ec['title']
            all_ec.append(ecs_)
        ues_['nbr_ec']=nbr
        ues_['ec']=all_ec
        all_ue.append(ues_)
    matiers['ue']=all_ue

    etudiants_ = crud.ancien_etudiant.get_by_class_limit(schemas,uuid_parcours,semestre,skip,limit)
    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    mention = crud.mention.get_by_uuid(db=db,uuid=uuid_mention)
    all_etudiant = []
    if len(etudiants_)==0:
        raise HTTPException(
            status_code=400,
            detail="Etudiants not fount.",
        )
    for etudiant in etudiants_: 
        print(etudiant['num_carte'])
        etudiants = {}
        etudiants["nom"]=etudiant["nom"]
        etudiants["prenom"]=etudiant["prenom"]
        etudiants["num_carte"]=etudiant['num_carte']
        all_etudiant.append(etudiants)

    data['mention']=mention.title
    data['parcours']=parcours.title
    data['anne']=decode_schemas(schemas)
    data['session']=session
    data['salle']=salle
    data['skip']=skip
    data['limit']=limit
    file = liste_exams.PDF.create_list_examen(semestre,parcours,data,matiers,etudiant)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)

@router.post("/list_inscrit/")
def list_inscrit(
    schemas:str,
    semestre:str,
    uuid_parcours:str,
    uuid_mention:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    create liste au examen
    """
    etudiants_ = crud.ancien_etudiant.get_by_class(schemas,uuid_parcours,semestre)
    parcours = crud.parcours.get_by_uuid(db=db,uuid=uuid_parcours)
    mention = crud.mention.get_by_uuid(db=db,uuid=uuid_mention)
    all_etudiant = []
    if etudiants_:
        for etudiant in etudiants_:
            etudiants = {}
            etudiants["nom"]=etudiant["nom"]
            etudiants["prenom"]=etudiant["prenom"]
            etudiants["num_carte"]=etudiant["num_carte"]
            all_etudiant.append(etudiants)

    data = {}
    data['mention']=mention.title
    data['parcours']=parcours.title
    data['anne']=decode_schemas(schemas)
    file = liste_inscrit.PDF.create_list_inscrit(semestre,parcours.abreviation,data,all_etudiant)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)