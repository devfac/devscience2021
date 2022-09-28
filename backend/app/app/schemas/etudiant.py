from typing import Optional
from uuid import UUID

from pydantic import BaseModel

keys = [
    "num_carte",
    "nom",
    "prenom",
    "date_naiss",
    "lieu_naiss",
    "adresse",
    "sexe",
    "nation",
    "num_cin",
    "date_cin",
    "lieu_cin",
    "montant",
    "bacc_anne",
    "etat",
    "photo",
    "num_quitance",
    "date_quitance",
    "uuid_mention",
    "uuid_journey"
]


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


class SelectEtudiantBase(BaseModel):
    uuid: Optional[UUID]
    num_select: Optional[str]
    nom: Optional[str] = None
    prenom: Optional[str] = None
    date_naiss: Optional[str] = None
    lieu_naiss: Optional[str] = None
    adresse: Optional[str] = None
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    lieu_cin: Optional[str] = None
    uuid_mention: Optional[str]
    niveau: Optional[str] = None
    sexe: Optional[str] = None
    nation: Optional[str] = None
    branche: Optional[str] = None
    select: Optional[bool] = False


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
    num_cin: Optional[str]
    date_cin: Optional[str]
    lieu_cin: Optional[str]
    montant: str
    moyenne: float
    bacc_anne: str
    etat: str
    photo: str
    num_quitance: str
    date_quitance: str
    uuid_mention: UUID
    uuid_journey: UUID
    semester_petit: str
    semester_grand: str


class EtudiantNouveauCreate(EtudiantBase):
    num_carte: str
    nom: str
    prenom: str
    date_naiss: str
    lieu_naiss: str
    adresse: str
    sexe: str
    situation: str
    telephone: str
    nation: str
    num_cin: Optional[str]
    date_cin: Optional[str]
    lieu_cin: Optional[str]
    montant: str
    num_quitance: str
    date_quitance: str
    photo: str
    bacc_num: str
    bacc_centre: str
    bacc_anne: str
    bacc_serie: str
    proffession: str
    nom_pere: Optional[str]
    proffession_pere: Optional[str]
    nom_mere: Optional[str]
    proffession_mere: Optional[str]
    adresse_parent: Optional[str]
    niveau: str
    branche: str
    uuid_mention: UUID
    uuid_journey: UUID


# Properties to receive via API on update
class EtudiantAncienUpdate(EtudiantBase):
    moyenne: Optional[float] = None
    num_carte: Optional[str]
    bacc_anne: Optional[str]
    uuid_mention: Optional[UUID]
    uuid_journey: Optional[UUID]
    semester_petit: Optional[str]
    semester_grand: Optional[str]


class EtudiantNouveauUpdate(EtudiantBase):
    num_carte: Optional[str]
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
    branche: Optional[str]
    niveau: Optional[str]
    uuid_mention: Optional[UUID]
    uuid_journey: Optional[UUID]
    select: Optional[bool] = True


class EtudiantAncienInDBBase(EtudiantBase):
    uuid: Optional[UUID]
    num_carte: Optional[str]
    bacc_anne: Optional[str]
    moyenne: Optional[float] = None
    semester_petit: Optional[str]
    semester_grand: Optional[str]

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
    branche: Optional[str]

    class Config:
        orm_mode = True


# Additional properties to return via API
class EtudiantAncien(EtudiantAncienInDBBase):
    journey: Optional[str]


# Additional properties stored in DB
class EtudiantAncienInDB(EtudiantAncienInDBBase):
    pass


class EtudiantNouveau(EtudiantNouveauInDBBase):
    pass


# Additional properties stored in DB
class EtudiantNouveauInDB(EtudiantNouveauInDBBase):
    pass


class EtudiantCarte(BaseModel):
    num_carte: str
    nom: str
    prenom: str
    date_naiss: str
    lieu_naiss: str
    num_cin: Optional[str]
    date_cin: Optional[str]
    lieu_cin: Optional[str]
    journey: str
