import os, sys
from typing import List
from fastapi import APIRouter, UploadFile, File

from app.components.file_handler import save_file_by_type
from app.components.data_ingestion import DataIngestion

from app.logger import logger


router = APIRouter()

@router.post("/upload/")
async def upload_file(files: List[UploadFile] = File(...)):
    try: 
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
    except Exception as e:
        logger.info(f"Exception occure during upload route store data : {str(e)}")
        return{"error": e}