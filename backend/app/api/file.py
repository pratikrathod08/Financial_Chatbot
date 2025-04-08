import os, sys
from typing import List
from fastapi import APIRouter, UploadFile, File

from app.components.file_handler import save_file_by_type
from app.components.data_ingestion import DataIngestion


router = APIRouter()

@router.post("/upload/")
async def upload_file(files: List[UploadFile] = File(...)):
    data_ingestion_class = DataIngestion()
    results = []
    data_store = []
    
    for file in files:
        result = await save_file_by_type(file)
        results.append(result)
    
    for file in results:
        result = data_ingestion_class.data_ingestion(file)
        data_store.append(result)
    return {"status": "success", "result": data_store}
