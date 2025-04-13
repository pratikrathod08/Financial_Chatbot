import os, sys
import shutil
import csv
from datetime import datetime
from fastapi import UploadFile

from app.logger import logger
from app.exception import CustomException

from dotenv import load_dotenv
load_dotenv()


UPLOAD_DIR = os.getenv("UPLOAD_DIR")
CSV_LOG_PATH = os.path.join(UPLOAD_DIR, "upload_log.csv")

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
    try: 
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

        # Prepare log entry
        log_entry = {
            "timestamp": timestamp,
            "original_filename": filename,
            "stored_as": new_filename,
            "file_type": file_type,
            "path": file_path
        }

        # Log to CSV file
        file_exists = os.path.isfile(CSV_LOG_PATH)
        with open(CSV_LOG_PATH, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["timestamp", "original_filename", "stored_as", "file_type", "path"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
            writer.writerow(log_entry)

        logger.info(log_entry)
        logger.info("File stored and logged successfully")

        return {
            "original_filename": filename,
            "stored_as": new_filename,
            "file_type": file_type,
            "path": file_path
        }
    
    except Exception as e: 
        logger.info(f"Exception occure during file write to local storage : {str(e)} ")
        raise CustomException(e, sys)

