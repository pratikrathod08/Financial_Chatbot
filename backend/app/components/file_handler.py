# app/components/file_handler.py
import os
from fastapi import UploadFile
from datetime import datetime
import shutil
from dotenv import load_dotenv

from app.logger import logger


load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")

EXTENSION_MAP = {
    '.csv': 'csv',
    '.xlsx': 'excel',
    '.xls': 'excel',
    '.pdf': 'pdf',
    '.docx': 'docx',
    '.doc': 'docx',
    '.txt': 'text'
}

async def save_file_by_type(file: UploadFile):
    logger.info("File storage started")
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    file_type = EXTENSION_MAP.get(ext, 'others')

    # Directory based on env variable
    type_dir = os.path.join(UPLOAD_DIR, file_type)
    os.makedirs(type_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{timestamp}_{filename}"
    file_path = os.path.join(type_dir, new_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info({
        "original_filename": filename,
        "stored_as": new_filename,
        "file_type": file_type,
        "path": file_path
    })
    logger.info("File stored successfully")

    return {
        "original_filename": filename,
        "stored_as": new_filename,
        "file_type": file_type,
        "path": file_path
    }
