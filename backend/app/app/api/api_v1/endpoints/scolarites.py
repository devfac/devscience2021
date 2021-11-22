from fastapi import APIRouter, Depends, File
from sqlalchemy.orm import Session
from app import models
from typing import Any
from app.api import deps
from fastapi.responses import FileResponse
from app.utils_sco.scolarite import create_certificat_scolarite

router = APIRouter()

@router.delete("/certificat")
def certificat(
    *,
    db: Session = Depends(deps.get_db),
    num_carte: str,
    schema: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any:
    data = {"nom":"RALAITSIMANOLAKAVANA","prenom":"Henri Franck",
            "date_naiss":"07 octobre 1995 ", "lieu_naiss":" Fianarantsoa",
            "niveau":"M2", "mention":"Mathématiques et Applications",
            "parcours":"Mathématiques et Informatiques pous la Sciences Social",
            "registre":"20"}

    
    file = create_certificat_scolarite(num_carte, 50,"2020", "2020-2021", data)
    return FileResponse(path=file, media_type='application/octet-stream', filename=file)