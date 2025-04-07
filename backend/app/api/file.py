# app/api/file.py
from fastapi import APIRouter, UploadFile, File
# from app.services.file_handler import handle_upload

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    return {"response": "This is response of upload route"}
