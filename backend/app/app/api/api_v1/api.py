from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, mentions, roles, parcours, \
    semestres, anne_univ, semestre_valide, ancien_etudiants, nouveau_etudiants, matier_ue, matier_ec, \
    scolarites, notes, notes_etudiants, liste, save_data, resultat, statistic, diplome, droit, carte, drive_action

api_router = APIRouter()
api_router.include_router(liste.router, prefix="/liste", tags=["liste"])
api_router.include_router(statistic.router, prefix="/statistic", tags=["statistic"])
api_router.include_router(save_data.router, prefix="/save_data", tags=["save_data"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(resultat.router, prefix="/resultat", tags=["resultat"])
api_router.include_router(notes_etudiants.router, prefix="/notes_etudiants", tags=["notes des etudiants"])
api_router.include_router(anne_univ.router, prefix="/anne_univ", tags=["anne universtitaire"])
api_router.include_router(mentions.router, prefix="/mentions", tags=["mentions"])
api_router.include_router(parcours.router, prefix="/parcours", tags=["parcours"])
api_router.include_router(semestres.router, prefix="/semestres", tags=["semestre"])
api_router.include_router(matier_ue.router, prefix="/matier_ue", tags=["unité d'enseignements"])
api_router.include_router(matier_ec.router, prefix="/matier_ec", tags=["éléments constitutif"])
api_router.include_router(ancien_etudiants.router, prefix="/ancien_etudiants", tags=["ancien etudiants"])
api_router.include_router(nouveau_etudiants.router, prefix="/nouveau_etudiants", tags=["nouveaux etudiants"])
api_router.include_router(semestre_valide.router, prefix="/semestre_valide", tags=["semestre valide"])
api_router.include_router(scolarites.router, prefix="/scolarites", tags=["scolarites"])
api_router.include_router(diplome.router, prefix="/diplome", tags=["diplome"])
api_router.include_router(droit.router, prefix="/droit", tags=["droits"])
api_router.include_router(carte.router, prefix="/carte", tags=["cartes"])
api_router.include_router(drive_action.router, prefix="/write_to_spreadsheet", tags=["spreadsheet"])
