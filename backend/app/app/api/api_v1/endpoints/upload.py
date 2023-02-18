import os
from os import getcwd
from typing import List

from fastapi import APIRouter, UploadFile, File
from starlette.responses import FileResponse

router = APIRouter()
@router.get("/")
def get_file(name_file: str, directory: str = "publication"):
    path = getcwd() + f"/files/{directory}" + name_file
    if os.path.exists(path):
        return FileResponse(path=path)


@router.post("/")
async def create_upload_file(
        *,
        uploaded_files: List[UploadFile] = File(...),
        directory: str = "publication"
        #current_user: models.User = Depends(deps.get_current_active_user)
        ):
    for uploaded_file in uploaded_files:
        name = uploaded_file.filename
        file_location = f"files/{directory}/{str(name).replace(' ', '_')}"
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
    return {"filenames": [str(file.filename).replace(' ', '_') for file in uploaded_files]}
