from typing import Any

from sqlalchemy.sql.functions import percentile_cont

from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email
from fastapi.responses import FileResponse
from app.liste import liste_exams, liste_inscrit,liste_bourese_passant
from app import crud
from app.utils import decode_schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/list_exam/")
def list_examen(
    schemas:str,
    semestre:str,
    uuid_parcours:str,
    uuid_mention:str,
    session:str,
    salle:str,
    skip:int =1,
    limit:int =100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    create liste au examen
    """
    data = {}
    matiers = {} 
    ues = crud.matier_ue.get_by_class(schemas,uuid_parcours,semestre)
    if len(ues)==0:
        raise HTTPException(
            status_code=400,
            detail="Matiers not fount.",
        )
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
    file = liste_exams.PDF.create_list_examen(semestre,parcours,data,matiers,all_etudiant)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)

@router.get("/list_inscrit/")
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

@router.get("/list_bourse/")
def list_bourse(
    schemas:str,
    uuid_mention:str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    create liste au examen
    """
    etat = "Passant"
    all_data = {}
    all_parcours = []
    mention = crud.mention.get_by_uuid(db=db,uuid=uuid_mention)
    if not mention:
        raise HTTPException(
            status_code=404,
            detail="The mention with this uuid does not exist in the system.",
        )
    parcours = crud.parcours.get_by_mention(db=db,uuid_mention=uuid_mention)
    all_data ['mention'] = mention.title
    for parcour in parcours:
        parcours_ = {}
        parcours_["name"] = parcour.title
        all_etudiant = []
        etudiants_ = crud.ancien_etudiant.get_by_parcours_and_etat(schema=schemas,uuid_parcours=str(parcour.uuid),etat=etat)
        if etudiants_:
            for etudiant in etudiants_:
                etudiants = {}
                etudiants["nom"]=etudiant["nom"]
                etudiants["prenom"]=etudiant["prenom"]
                etudiants["num_carte"]=etudiant["num_carte"]
                all_etudiant.append(etudiants)
        parcours_["etudiant"] =all_etudiant
        all_parcours.append(parcours_)
    all_data['parcour'] = all_parcours
    all_data['anne'] = decode_schemas(schemas)

    print(all_data)
    file = liste_bourese_passant.PDF.create_list_bourse_passant(mention.title,all_data)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)