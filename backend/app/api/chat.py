# app/api/file.py
from fastapi import APIRouter, UploadFile, File
# from app.services.file_handler import handle_upload
from app.logger import logging

router = APIRouter()

@router.post("/chat/")
async def upload_file(file: UploadFile = File(...)):
    logging.info("Chat route started")
    return {"Response": "This is chat route"}
