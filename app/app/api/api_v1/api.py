from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, mentions, roles, \
    college_year,matier_ue, matier_ec, \
    scolarites, notes, liste, save_data, resultat, statistic, diploma, enrollment_fee, carte, drive_action,\
    student, interaction, invitation, permission, classroom, bacc_serie, historic, upload, validation,\
    subscription, user_mention, journey

api_router = APIRouter()
api_router.include_router(interaction.router, prefix="/interaction", tags=["interaction"])
api_router.include_router(user_mention.router, prefix="/user_mention", tags=["user mention"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(bacc_serie.router, prefix="/bacc_serie", tags=["Bacc serie"])
api_router.include_router(classroom.router, prefix="/classroom", tags=["classroom"])
api_router.include_router(invitation.router, prefix="/invitation", tags=["invitation"])
api_router.include_router(permission.router, prefix="/permission", tags=["permission"])
api_router.include_router(liste.router, prefix="/liste", tags=["liste"])
api_router.include_router(historic.router, prefix="/historic", tags=["historic"])
api_router.include_router(statistic.router, prefix="/statistic", tags=["statistic"])
api_router.include_router(save_data.router, prefix="/save_data", tags=["save_data"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(matier_ue.router, prefix="/matier_ue", tags=["unité d'enseignement"])
api_router.include_router(matier_ec.router, prefix="/matier_ec", tags=["élément constitutif"])
api_router.include_router(resultat.router, prefix="/resultat", tags=["resultat"])
api_router.include_router(college_year.router, prefix="/college_year", tags=["College year"])
api_router.include_router(mentions.router, prefix="/mentions", tags=["mentions"])
api_router.include_router(journey.router, prefix="/journey", tags=["Journeys"])
api_router.include_router(student.router, prefix="/student", tags=["students"])
api_router.include_router(subscription.router, prefix="/subscription", tags=["subscription"])
api_router.include_router(validation.router, prefix="/validation", tags=["validation"])
api_router.include_router(scolarites.router, prefix="/scolarites", tags=["scolarites"])
api_router.include_router(diploma.router, prefix="/diplome", tags=["diplome"])
api_router.include_router(enrollment_fee.router, prefix="/enrollment_fee", tags=["enrollment_fee"])
api_router.include_router(carte.router, prefix="/carte", tags=["cartes"])
api_router.include_router(drive_action.router, prefix="/write_to_spreadsheet", tags=["spreadsheet"])
