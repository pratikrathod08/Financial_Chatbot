import os, sys
from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
import pandas as pd
import mimetypes
import PyPDF2
import docx

from app.utils.chat_utils import run_sql_query
from app.schemas.chat_schema import AskRequest
from app.components.vectorstore import VectorStore

from dotenv import load_dotenv
load_dotenv()


router = APIRouter()

@router.post("/ask/")
async def ask_files(request: AskRequest):
    vectordb=VectorStore()
    results = vectordb.search_similar(request.query)
    response_data = [doc.page_content for doc in results]
    print("This is response data : ", response_data)
    return {"Result": response_data}
    # print(f"This is result : {results}")
    # return {"Result": str(results)}
