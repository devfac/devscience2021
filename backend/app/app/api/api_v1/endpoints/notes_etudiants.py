from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils import decode_schemas, get_credit, max_value
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/insert_etudiants/", response_model=List[Any])
def inserts_etudiant(
        *,
        db: Session = Depends(deps.get_db),
        schemas: str,
        semestre: str,
        session: str,
        uuid_parcours: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schemas))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.",
                            )

    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    all_note = []
    test_note = crud.note.check_table_exist(schemas, semestre, parcours.abbreviation, session)
    if not test_note:
        raise HTTPException(
            status_code=400,
            detail=f"note_{parcours.abbreviation.lower()}_{semestre.lower()}_{session.lower()} not found.",
        )

    if session.lower() == "rattrapage":
        test_note = crud.note.check_table_exist(schemas, semestre, parcours.abbreviation, "normal")
        if not test_note:
            raise HTTPException(status_code=400,
                                detail=f"note_{parcours.abbreviation.lower()}_{semestre.lower()}_normal not found.",
                                )
        credit = 30
        all_etudiant = crud.note.read_by_credit(schemas, semestre, parcours.abbreviation, "normal", credit)
        for etudiant in all_etudiant:
            et_un = crud.note.read_by_num_carte(schemas, semestre, parcours.abbreviation, session, etudiant.num_carte)
            if not et_un:
                crud.note.insert_note(schemas, semestre, parcours.abbreviation, session, etudiant.num_carte)
                crud.note.update_auto(schemas, semestre, parcours.abbreviation, session, etudiant.num_carte)
        all_note = crud.note.read_all_note(schemas, semestre, parcours.abbreviation, session)
        return all_note

    else:
        list = crud.ancien_etudiant.get_by_class(schemas, uuid_parcours, semestre)
        if list is not None:
            for etudiant in list:
                et_un = crud.note.read_by_num_carte(schemas, semestre, parcours.abbreviation, session,
                                                    etudiant.num_carte)
                if not et_un:
                    crud.note.insert_note(schemas, semestre, parcours.abbreviation, session, etudiant.num_carte)
                    crud.note.insert_note(schemas, semestre, parcours.abbreviation, "final", etudiant.num_carte)
        all_note = crud.note.read_all_note(schemas, semestre, parcours.abbreviation, session)
        return all_note


@router.get("/get_all_notes/", response_model=List[Any])
def get_all_notes(
        *,
        db: Session = Depends(deps.get_db),
        schemas: str,
        semestre: str,
        session: str,
        uuid_parcours: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schemas))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.",
                            )

    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")

    all_note = crud.note.read_all_note(schemas, semestre, parcours.abbreviation, session)
    return all_note


@router.post("/insert_note", response_model=List[Any])
def updates_note(
        *,
        db: Session = Depends(deps.get_db),
        schemas: str,
        semestre: str,
        session: str,
        uuid_parcours: str,
        all_notes_ue: List[List[schemas.Note]],
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """

    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schemas))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.",
                            )

    parcours = crud.parcours.get_by_uuid(db=db, uuid=uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre, parcours=parcours.abbreviation,
                                            session=session)
    if not test_note:
        raise HTTPException(status_code=400,
                            detail=f"note_{parcours.abbreviation.lower()}_{semestre.lower()}_{session.lower()} not found.",
                            )
    moy_cred_in = {}
    moy_cred_in_fin = {}
    for notes in all_notes_ue:
        for note in notes:
            et_un = crud.note.read_by_num_carte(schemas, semestre, parcours.abbreviation, session, note.num_carte)
            et_un_final = crud.note.read_by_num_carte(schemas, semestre, parcours.abbreviation, "final", note.num_carte)
            if et_un:
                ue_in = {}
                ue_in_final = {}
                ecs = crud.matier_ec.get_by_value_ue(schemas, note.name, semestre, uuid_parcours)
                note_ue = 0
                note_ue_final = 0
                credit = crud.matier_ue.get_by_value(schemas, note.name, semestre, uuid_parcours).credit
                if len(note.ec) != len(ecs):
                    raise HTTPException(status_code=400, detail="ivalide EC for UE",
                                        )
                for i, ec in enumerate(ecs):
                    ec_note = note.ec[i].note
                    if ec_note == "":
                        note.ec[i].note = None
                        value_ec_note = 0
                    else:
                        value_ec_note = float(note.ec[i].note)

                    value_sess = et_un_final[f'ec_{note.ec[i].name}']
                    if value_sess is None:
                        value_sess = 0
                    poids_ec = crud.matier_ec.get_by_value(schemas, ecs[i][2], semestre, uuid_parcours)
                    note_ue += value_ec_note * float(poids_ec.poids)
                    note_ue_final += max_value(value_ec_note, value_sess) * float(poids_ec.poids)
                ue_in[f'ue_{note.name}'] = note_ue
                ue_in_final[f'ue_{note.name}'] = note_ue_final
                for note_ec in note.ec:
                    value_sess = et_un_final[f'ec_{note_ec.name}']
                    if value_sess is None:
                        value_sess = 0
                    ue_in[f'ec_{note_ec.name}'] = note_ec.note
                    ue_in_final[f'ec_{note_ec.name}'] = max_value(note_ec.note, value_sess)
                    print(max_value(note_ec.note, value_sess))

                crud.note.update_note(schemas, semestre, parcours.abbreviation, session, note.num_carte, ue_in)
                crud.note.update_note(schemas, semestre, parcours.abbreviation, "final", note.num_carte, ue_in_final)
                et_un = crud.note.read_by_num_carte(schemas, semestre, parcours.abbreviation, session, note.num_carte)
                et_un_final = crud.note.read_by_num_carte(schemas, semestre, parcours.abbreviation, "final",
                                                          note.num_carte)
                ues = crud.matier_ue.get_by_class(schemas, uuid_parcours, semestre)
                moy = 0
                credit = 0
                moy_fin = 0
                credit_fin = 0
                somme = 0
                for ue in ues:
                    value_sess = et_un[f'ue_{ue.value}']
                    if value_sess is None:
                        value_sess = 0
                    value_fin = et_un_final[f'ue_{ue.value}']
                    if value_fin is None:
                        value_fin = 0
                    somme += ue.credit
                    moy += float(value_sess) * ue.credit
                    credit += get_credit(float(value_sess), ue.credit)

                    moy_fin += float(value_fin) * ue.credit
                    credit_fin += get_credit(float(value_fin), ue.credit)

                    moy_cred_in["moyenne"] = moy / somme
                    moy_cred_in["credit"] = credit

                    moy_cred_in_fin["moyenne"] = moy_fin / somme
                    moy_cred_in_fin["credit"] = credit_fin

                    crud.note.update_note(schemas, semestre, parcours.abbreviation, session, note.num_carte, moy_cred_in)
                    crud.note.update_note(schemas, semestre, parcours.abbreviation, "final", note.num_carte, moy_cred_in)

    all_note = crud.note.read_all_note(schemas, semestre, parcours.abbreviation, session)
    return all_note


@router.delete("/", response_model=List[Any])
def delete_note(
        *,
        db: Session = Depends(deps.get_db),
        schemas: str,
        semestre: str,
        uuid_parcours: str,
        num_carte: str,
        session: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create table note.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schemas))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schemas)} not found.",
                            )

    parcours = crud.parcours.get_by_uuid(db, uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail="Parcours not found")
    test_note = crud.note.check_table_exist(schemas=schemas, semestre=semestre, parcours=parcours.abbreviation,
                                            session=session)
    if not test_note:
        raise HTTPException(status_code=400,
                            detail=f"note_{parcours.abbreviation.lower()}_{semestre.lower()}_{session.lower()} not found.",
                            )
    et_un = crud.note.read_by_num_carte(schemas, semestre, parcours.abbreviation, session, num_carte)
    if et_un:
        crud.note.delete_by_num_carte(schemas, semestre, parcours.abbreviation, num_carte)
    all_note = crud.note.read_all_note(schemas, semestre, parcours.abbreviation)
    return all_note
