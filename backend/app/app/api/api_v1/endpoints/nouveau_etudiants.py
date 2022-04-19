from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder
from app import crud, models, schemas
from app.api import deps
from app.utils import decode_schemas, create_num_carte, get_sems_min, get_sems_max

router = APIRouter()


@router.get("/", response_model=List[Any])
def read_etudiant_nouveau(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve etudiant nouveau.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.",
                            )
    etudiant = crud.nouveau_etudiant.get_all(schema=schema)

    return etudiant


@router.post("/", response_model=List[Any])
def create_select_etudiant_nouveau(
        *,
        db: Session = Depends(deps.get_db),
        etudiant_in: schemas.SelectEtudiantBase,
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new etudiant.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )

    etudiant_in.uuid = uuid.uuid4()
    mention = crud.mention.get_by_uuid(db=db, uuid=etudiant_in.uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )
    all_etutiant = crud.nouveau_etudiant.get_by_mention(schema, etudiant_in.uuid_mention)
    etudiant_in.num_select = f"S{mention.abreviation.upper()}{etudiant_in.num_select}"
    etudiant = crud.nouveau_etudiant.create_etudiant(schema=schema, obj_in=etudiant_in)
    return etudiant


@router.put("/update_etudiant/", response_model=List[Any])
def update_etudiant(
        *,
        db: Session = Depends(deps.get_db),
        num_carte: str,
        schema: str,
        etudiant_in: schemas.EtudiantNouveauUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an etudiant.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )

    etudiant = crud.nouveau_etudiant.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    etudiant = crud.nouveau_etudiant.update_etudiant(schema=schema, num_carte=num_carte, obj_in=etudiant_in)
    return etudiant


@router.put("/update_etudiant_by_num_select/", response_model=List[Any])
def update_etudiant(
        *,
        db: Session = Depends(deps.get_db),
        num_select: str,
        schema: str,
        etudiant_in: schemas.SelectEtudiantBase,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an etudiant.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )

    etudiant = crud.nouveau_etudiant.get_by_num_select(schema=schema, num_select=num_select)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    etudiant = crud.nouveau_etudiant.update_etudiant_select(schema=schema, num_select=num_select, obj_in=etudiant_in)
    return etudiant


@router.put("/update_etudiant_by_num_select_admis/", response_model=List[Any])
def update_etudiant(
        *,
        db: Session = Depends(deps.get_db),
        num_select: str,
        schema: str,
        etudiant_in: schemas.EtudiantNouveauUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an etudiant.
    
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )

    etudiant = crud.nouveau_etudiant.get_by_num_select(schema=schema, num_select=num_select)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    mention = crud.mention.get_by_uuid(db=db, uuid=etudiant.uuid_mention)
    if not mention:
        raise HTTPException(status_code=400, detail=f" Mention not found.", )

    parcours = crud.parcours.get_by_uuid(db=db, uuid=etudiant_in.uuid_parcours)
    if not parcours:
        raise HTTPException(status_code=400, detail=f" Parcours not found.", )

    all_etudiant = crud.nouveau_etudiant.get_by_num_select_admis(schema=schema, branche=etudiant.branche)
    num = int(mention.last_num_carte) + len(all_etudiant) + 1
    if not etudiant.num_carte:
        etudiant_in.num_carte = create_num_carte(etudiant.branche, str(num))

    etudiant_in.uuid_mention = mention.uuid
    etudiant_in.branche = mention.branche

    etudiants = crud.nouveau_etudiant.update_etudiant_select(schema=schema, num_select=num_select, obj_in=etudiant_in)

    etudiant = crud.nouveau_etudiant.get_by_num_select(schema=schema, num_select=num_select)
    etudiant_create = {}
    for key in schemas.keys:
        etudiant_create[key] = jsonable_encoder(etudiant)[key]
    etudiant_create["semestre_petit"] = get_sems_min(jsonable_encoder(etudiant)["niveau"])
    etudiant_create["semestre_grand"] = get_sems_max(jsonable_encoder(etudiant)["niveau"])
    etudiant_ = crud.ancien_etudiant.get_by_num_carte(schema=schema, num_carte=etudiant_create["num_carte"])
    if etudiant_:
        etudiant = crud.ancien_etudiant.update_etudiant(schema=schema, num_carte=etudiant_create["num_carte"],
                                                        obj_in=etudiant_create)
    else:
        etudiant_create["uuid"] = uuid.uuid4()
        etudiant = crud.ancien_etudiant.create_etudiant(schema=schema, obj_in=etudiant_create)

    return etudiants


@router.get("/by_num_carte/", response_model=Any)
def read_etudiant_by_num_carte(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        num_carte: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by num insription.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )
    etudiant = crud.nouveau_etudiant.get_by_num_carte(schema=schema, num_carte=num_carte)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return etudiant


@router.get("/by_num_select/", response_model=schemas.SelectEtudiantBase)
def read_etudiant_by_num_select(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        num_select: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by num insription.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )
    etudiant = crud.nouveau_etudiant.get_by_num_select(schema=schema, num_select=num_select)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return etudiant


@router.get("/by_mention/", response_model=List[Any])
def read_etudiant_by_mention(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid_mention: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by mention.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )
    etudiant = crud.nouveau_etudiant.get_by_mention(schema=schema, uuid_mention=uuid_mention)

    return etudiant


@router.get("/by_parcours/", response_model=List[Any])
def read_etudiant_by_mention(
        *,
        db: Session = Depends(deps.get_db),
        schema: str,
        uuid_parcours: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get etudiant by parcours.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )
    etudiant = crud.nouveau_etudiant.get_by_parcours(schema=schema, uuid_parcours=uuid_parcours)
    return etudiant


@router.delete("/", response_model=List[Any])
def delete_etudiant_nouveau(
        *,
        db: Session = Depends(deps.get_db),
        num_select: str,
        schema: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an etudiant.
    """
    anne_univ = crud.anne_univ.get_by_title(db, decode_schemas(schema=schema))
    if not anne_univ:
        raise HTTPException(status_code=400, detail=f"{decode_schemas(schema=schema)} not found.", )
    etudiant = crud.nouveau_etudiant.get_by_num_select(schema=schema, num_select=num_select)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Etudiant not found")

    etudiant = crud.nouveau_etudiant.delete_etudiant(schema=schema, num_select=num_select)
    return etudiant
