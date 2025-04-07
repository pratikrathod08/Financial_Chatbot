from fastapi import APIRouter, Request
from pydantic import BaseModel
import os
from typing import List
import pandas as pd
import PyPDF2
import docx
import mimetypes

from app.utils.chat_utils import *
from app.schemas.chat_schema import AskRequest

from dotenv import load_dotenv


load_dotenv()

router = APIRouter()
UPLOAD_FOLDER = os.getenv("UPLOAD_DIR")


@router.post("/ask/")
async def ask_files(request: AskRequest):
    all_text = ""
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        mime, _ = mimetypes.guess_type(path)

        if mime:
            if mime == "application/pdf":
                all_text += read_pdf(path) + "\n"
            elif mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                all_text += read_docx(path) + "\n"
            elif mime == "text/csv":
                all_text += read_csv(path) + "\n"
            elif mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                all_text += read_excel(path) + "\n"
            elif mime.startswith("text"):
                all_text += read_txt(path) + "\n"
    
    if not all_text:
        return {"answer": "No readable files found."}

    # Very basic answer logic (replace with LLM or RAG later)
    if request.query.lower() in all_text.lower():
        return {"answer": f"Yes, your query was found in the content."}
    else:
        return {"answer": "Sorry, nothing relevant found."}
