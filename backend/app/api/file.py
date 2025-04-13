import os, sys
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form

from app.components.file_handler import save_file_by_type, save_url_files
from app.components.data_ingestion import DataIngestion

from app.logger import logger


router = APIRouter()

@router.post("/upload/")
async def upload_file(
    files: List[UploadFile] = File(None), 
    url: Optional[str] = Form(None)
    ):
    try: 
        if files:
            logger.info("file uploaded from frontend")
            data_ingestion_class = DataIngestion()
            results = []
            for file in files:
                result = await save_file_by_type(file)
                results.append(result)
            logger.info("file storage completed ")
            logger.info(f"Results stored : {str(results)}")
            for file in results:
                data_ingestion_class.data_ingestion(file)
            logger.info("Data ingestion completed of all files: ")
            return {"status": "success"}
        elif url:
            logger.info("Url uploaded from frontend")
            data_ingestion_class = DataIngestion()
            results = await save_url_files(url)
            logger.info(f"Results stored : {str(results)}")
            for file in results:
                data_ingestion_class.data_ingestion(file)
            logger.info("Data ingestion completed of all files: ")
            return {"status": "success"}
        else:
            return {"error": "No files or URL provided"}

    except Exception as e:
        logger.info(f"Exception occure during upload route store data : {str(e)}")
        return{"error": e}