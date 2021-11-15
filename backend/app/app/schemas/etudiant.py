from typing import Optional, Any
from uuid import uuid4, UUID
from sqlalchemy.sql.sqltypes import String

from pydantic import BaseModel, EmailStr


# Shared properties
class EtudiantBase(BaseModel):
    uuid: Optional[UUID]
    nom: Optional[str] = None
    prenom: Optional[str] = None
    date_naiss: Optional[str] = None
    lieu_naiss: Optional[str] = None
    adresse: Optional[str] = None
    sexe: Optional[str] = None
    nation: Optional[str] = None
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    lieu_cin: Optional[str] = None
    montant: Optional[str] = None
    etat: Optional[str] = None
    photo: Optional[str] = None
    num_quitance: Optional[str] = None
    date_quitance: Optional[str] = None


# Properties to receive via API on creation
class EtudiantAncienCreate(EtudiantBase):
    num_carte: str
    nom: str
    prenom: str
    date_naiss: str
    lieu_naiss: str
    adresse: str
    sexe: str
    nation: str
    num_cin: str
    date_cin: str
    lieu_cin: str
    montant: str
    moyenne: float
    bacc: str
    etat: str
    photo: str
    num_quitance: str
    date_quitance: str
    uuid_mention: UUID
    uuid_parcours: UUID
    semestre_petit: str
    semestre_grand: str


class EtudiantNouveauCreate(EtudiantBase):
    num_insc: str
    nom: str
    prenom: str
    date_naiss: str
    lieu_naiss: str
    adresse: str
    sexe: str
    situation: str
    telephone: str
    nation: str
    num_cin: str
    date_cin: str
    lieu_cin: str
    montant: str
    num_quitance: str
    date_quitance: str
    photo: str
    bacc_num: str
    bacc_centre: str
    bacc_anne: str
    bacc_serie: str
    proffession: str
    nom_pere: str
    proffession_pere: str
    nom_mere: str
    proffession_mere: str
    adresse_parent: str
    niveau: str
    uuid_mention: UUID
    uuid_parcours: UUID
# Properties to receive via API on update
class EtudiantAncienUpdate(EtudiantBase):
    moyenne: Optional[float] = None
    num_carte: Optional[str]
    bacc:Optional[str]
    uuid_mention: Optional[UUID]
    uuid_parcours: Optional[UUID]
    semestre_petit: Optional[str]
    semestre_grand: Optional[str]

class EtudiantNouveauUpdate(EtudiantBase):
    num_insc: Optional[str]
    situation: Optional[str]
    telephone: Optional[str]
    bacc_num: Optional[str]
    bacc_centre: Optional[str]
    bacc_anne: Optional[str]
    bacc_serie: Optional[str]
    proffession: Optional[str]
    nom_pere: Optional[str]
    proffession_pere: Optional[str]
    nom_mere: Optional[str]
    proffession_mere: Optional[str]
    adresse_parent: Optional[str]
    niveau: Optional[str]
    uuid_mention: Optional[UUID]
    uuid_parcours: Optional[UUID]


class EtudiantAncienInDBBase(EtudiantBase):
    uuid: Optional[UUID]
    num_carte: Optional[str]
    moyenne: Optional[float] = None
    semestre_petit: Optional[str]
    semestre_grand: Optional[str]

    class Config:
        orm_mode = True

class EtudiantNouveauInDBBase(EtudiantBase):
    uuid: Optional[UUID]
    num_carte: Optional[str]
    bacc_num: Optional[str]
    bacc_centre: Optional[str]
    bacc_anne: Optional[str]
    bacc_serie: Optional[str]
    proffession: Optional[str]
    nom_pere: Optional[str]
    proffession_pere: Optional[str]
    nom_mere: Optional[str]
    proffession_mere: Optional[str]
    adresse_parent: Optional[str]
    niveau: Optional[str]

    class Config:
        orm_mode = True


# Additional properties to return via API
class EtudiantAncien(EtudiantAncienInDBBase):
    parcours:Optional[str]


# Additional properties stored in DB
class EtudiantAncienInDB(EtudiantAncienInDBBase):
    pass

class EtudiantNouveau(EtudiantNouveauInDBBase):
    pass

# Additional properties stored in DB
class EtudiantNouveauInDB(EtudiantNouveauInDBBase):
    pass
