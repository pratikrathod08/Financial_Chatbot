# app/api/file.py
from fastapi import APIRouter, UploadFile, File
from typing import List
# from app.services.file_handler import handle_upload
from app.components.file_handler import save_file_by_type


router = APIRouter()

@router.post("/upload/")
async def upload_file(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        result = await save_file_by_type(file)
        results.append(result)
    return {"status": "success", "files": results}
