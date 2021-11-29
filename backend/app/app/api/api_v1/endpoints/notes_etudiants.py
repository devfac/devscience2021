from typing import Any, List


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils import get_credit, max_value
from app import crud, models, schemas
from app.api import deps
import json

router = APIRouter()

@router.post("/insert_etudiants", response_model=List[Any])
def inserts_etudiant(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre:str,
    parcours:str,
    session:str,
    uuid_parcours:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """ 
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours,session=session)
    if not test_note:
        raise HTTPException( status_code=400, detail=f"note_{semestre}_{parcours}_{session} not found.",
        )

    all_note = []
    list = crud.ancien_etudiant.get_by_class(schemas,uuid_parcours,semestre)
    if list is not None:
        for etudiant in list:
            et_un = crud.note.read_by_num_carte(schemas, semestre, parcours,session,etudiant.num_carte)
            if not et_un:
                crud.note.insert_note(schemas,semestre,parcours,session,etudiant.num_carte)
                crud.note.insert_note(schemas,semestre,parcours,"final",etudiant.num_carte)
    all_note = crud.note.read_all_note(schemas, semestre, parcours,session)
    for note in all_note:
        print(note["ue_analyse"])
    return all_note


@router.post("/insert_note", response_model=List[Any])
def updates_note(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre: str,
    parcours:str,
    session:str,
    uuid_parcours:str,
    notes:List[schemas.Note],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """ 
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours,session=session)
    if not test_note:
        raise HTTPException( status_code=400, detail=f"note_{semestre}_{parcours}_{session} not found.",
        )
    moy_cred_in = {}
    moy_cred_in_fin = {}
    for note in notes:
        et_un = crud.note.read_by_num_carte(schemas, semestre, parcours,session,note.num_carte)
        et_un_final = crud.note.read_by_num_carte(schemas, semestre, parcours,"final",note.num_carte)
        if et_un:
            ue_in = {}
            ue_in_final = {}
            ecs = crud.matier_ec.get_by_value_ue(schemas,note.name,semestre,uuid_parcours)
            note_ue = 0
            note_ue_final = 0
            credit = crud.matier_ue.get_by_value(schemas,note.name,semestre,uuid_parcours).credit
            for i,ec in enumerate(ecs):
                value_sess = et_un_final[f'ec_{note.ec[i].name}']
                if value_sess == None:
                    value_sess =0
                poids_ec = crud.matier_ec.get_by_value(schemas,ecs[i][2],semestre,uuid_parcours)
                note_ue += float(note.ec[i].note)*float(poids_ec.poids)
                note_ue_final += max_value(float(note.ec[i].note),value_sess)*float(poids_ec.poids)
            ue_in[f'ue_{note.name}'] = note_ue
            ue_in_final[f'ue_{note.name}'] = note_ue_final
            for note_ec in note.ec:
                value_sess = et_un_final[f'ec_{note_ec.name}']
                if value_sess == None:
                    value_sess =0
                ue_in[f'ec_{note_ec.name}'] = note_ec.note
                ue_in_final[f'ec_{note_ec.name}'] = max_value(note_ec.note,value_sess )
        
            crud.note.update_note(schemas,semestre,parcours,session,note.num_carte,ue_in)
            crud.note.update_note(schemas,semestre,parcours,"final",note.num_carte,ue_in_final)
            et_un = crud.note.read_by_num_carte(schemas, semestre, parcours,session,note.num_carte)
            et_un_final = crud.note.read_by_num_carte(schemas, semestre, parcours,"final",note.num_carte)
            ues = crud.matier_ue.get_by_class(schemas,uuid_parcours,semestre)
            moy = 0
            credit = 0
            moy_fin = 0
            credit_fin = 0
            somme = 0
            for ue in ues:
                value_sess = et_un[f'ue_{ue.value}']
                if value_sess == None:
                    value_sess =0
                value_fin = et_un_final[f'ue_{ue.value}']
                if value_fin == None:
                    value_fin =0
                somme += ue.credit
                moy += float(value_sess)*ue.credit
                credit += get_credit(float(value_sess),ue.credit)

                moy_fin += float(value_fin)*ue.credit
                credit_fin += get_credit(value_fin,ue.credit)

                moy_cred_in["moyenne"]=moy/somme
                moy_cred_in["credit"]=credit

                moy_cred_in_fin["moyenne"]=moy_fin/somme
                moy_cred_in_fin["credit"]=credit_fin

                crud.note.update_note(schemas,semestre,parcours,session,note.num_carte,moy_cred_in)
                crud.note.update_note(schemas,semestre,parcours,"final",note.num_carte,moy_cred_in)


        
    all_note = crud.note.read_all_note(schemas, semestre, parcours,session)
    return all_note


@router.delete("/", response_model=List[Any])
def delete_note(
    *,
    db: Session = Depends(deps.get_db),
    schemas: str,
    semestre: str,
    parcours:str,
    num_carte:str,
    session:str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre,parcours=parcours,session=session)
    if not test_note:
        raise HTTPException( status_code=400, detail=f"note_{semestre}_{parcours}_{session} not found.",
        )
    et_un = crud.note.read_by_num_carte(schemas, semestre, parcours,session,num_carte)
    if et_un:
        crud.note.delete_by_num_carte(schemas,semestre,parcours,num_carte)
    all_note = crud.note.read_all_note(schemas, semestre, parcours)
    return all_note
