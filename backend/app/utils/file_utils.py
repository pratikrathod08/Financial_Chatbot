import os, sys
import csv
from datetime import datetime

import docx
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

from app.logger import logger 
from app.exception import CustomException

from dotenv import load_dotenv
load_dotenv()


UPLOAD_DIR = os.getenv("UPLOAD_DIR")
LOG_PATH = os.path.join(UPLOAD_DIR, "file_content_log.csv")

def log_file_data(file_path: str, content: str | pd.DataFrame):
    filename = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(content, pd.DataFrame):
        content_str = content.head(5).to_string(index=False)  # log preview only
    else:
        content_str = content[:1000]  # Limit large text logs for performance

    # Check if log file exists
    file_exists = os.path.isfile(LOG_PATH)

    with open(LOG_PATH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "filename", "content_preview"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": timestamp,
            "filename": filename,
            "content_preview": content_str
        })

logger.info("Data Extraction of file started")

def read_txt(path):
    try: 
        logger.info(f"Data Extraction of txt {path} file started")
        with open(path, "r", encoding="utf-8") as f:
            log_file_data(path, str(f.read()))
            return f.read()
    except Exception as e: 
        logger.info(f"Exception occure during Extraction of txt {path}") 
        raise CustomException(e, sys)
        
def extract_text_from_pdf(file_path: str) -> str:
    try:
        logger.info(f"Data Extraction of pdf {file_path} file started") 
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        log_file_data(file_path, str(text))    
        return text
    except Exception as e: 
        logger.info(f"Exception occure during Extraction of pdf {file_path}") 
        raise CustomException(e, sys)
    
def extract_text_from_docx(file_path: str) -> str:
    try:
        logger.info(f"Data Extraction of doc {file_path} file started") 
        doc = docx.Document(file_path)
        log_file_data(file_path, str("\n".join([para.text for para in doc.paragraphs])))
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e: 
        logger.info(f"Exception occure during Extraction of docx {file_path}") 
        raise CustomException(e, sys)    

def extract_text_from_csv(file_path: str):
    try:
        logger.info(f"Data Extraction of csv {file_path} file started")
        df = pd.read_csv(file_path)
        log_file_data(file_path, df) 
        return df
    except Exception as e: 
        logger.info(f"Exception occure during Extraction of csv {file_path}") 
        raise CustomException(e, sys)

def extract_text_from_excel(file_path: str):
    try:
        logger.info(f"Data Extraction of excel {file_path} file started") 
        df = pd.read_excel(file_path)
        log_file_data(file_path, df)
        return df
    except Exception as e: 
        logger.info(f"Exception occure during Extraction of excel {file_path}") 
        raise CustomException(e, sys)





