import os, sys
import uuid 
from datetime import datetime
import csv

from app.utils.file_utils import (read_txt, extract_text_from_pdf, 
                                  extract_text_from_csv, extract_text_from_excel, 
                                  extract_text_from_docx, extract_from_url)
from app.logger import logger
from app.exception import CustomException
from dotenv import load_dotenv
load_dotenv()


UPLOAD_DIR = os.getenv("UPLOAD_DIR")
txt_dir = os.path.join(UPLOAD_DIR, "txt")
csv_dir = os.path.join(UPLOAD_DIR, "csv")
CSV_LOG_PATH = os.path.join(UPLOAD_DIR, "upload_log.csv")

# Ensure directories exist
os.makedirs(txt_dir, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)


class DataExtractor:
    def __init__(self):
        logger.info("dataextraction endpoint hit")
        pass 

    logger.info("Data Extraction started")    
    def extract_text(self, file_path: str) -> str:
        logger.info("Text extraction started")
        if file_path.endswith(".pdf"):
            return extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            return extract_text_from_docx(file_path)
        elif file_path.endswith(".txt"):
            return read_txt(file_path)
        else:
            logger.info("Unsupported file type")
            raise ValueError("Unsupported file type")
        
    def extract_df(self, file_path: str):
        logger.info("DF Extraction started")
        if file_path.endswith(".csv"):
            logger.info("Returned df")
            return extract_text_from_csv(file_path)
        elif file_path.endswith(".xlsx"):
            logger.info("Returned df")
            return extract_text_from_excel(file_path)
        else:
            logger.info("Unsupported file type")
            raise ValueError("Unsupported file type")

    def extract_url(self, url: str):
        logger.info("URL Extraction Started")
        try:
            result = extract_from_url(url)
            text = result.get("text", "")
            tables = result.get("tables", [])

            file_details = []

            if text: 
                # Save text to txt_dir
                original_text_name = "extracted_text.txt"
                new_text_filename = f"{uuid.uuid4().hex}.txt"
                text_path = os.path.join(txt_dir, new_text_filename)
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(text)

                file_details.append({
                    "original_filename": original_text_name,
                    "stored_as": new_text_filename,
                    "file_type": "txt",
                    "path": text_path
                })

                ## ------------------------------------   Store log to csv started -----------------------

                # Directory based on env variable
                type_dir = os.path.join(UPLOAD_DIR, "txt")
                os.makedirs(type_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f"{timestamp}_{new_text_filename}"
                file_path = os.path.join(type_dir, new_filename)

                # Prepare log entry
                log_entry = {
                    "timestamp": timestamp,
                    "original_filename": original_text_name,
                    "stored_as": new_filename,
                    "file_type": "txt",
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

            ## ----------------------------- store log to csv closed ---------------------------

            if tables: 
                # Save tables to csv_dir
                for i, table in enumerate(tables):
                    original_table_name = f"{uuid.uuid4().hex}.csv"
                    new_csv_filename = original_table_name
                    csv_path = os.path.join(csv_dir, new_csv_filename)

                    if hasattr(table, "to_csv"):
                        table.to_csv(csv_path, index=False)
                    else:
                        import pandas as pd
                        pd.DataFrame(table).to_csv(csv_path, index=False)

                    file_details.append({
                        "original_filename": original_table_name,
                        "stored_as": new_csv_filename,
                        "file_type": "csv",
                        "path": csv_path
                    })

                    ## ------------------------------------   Store log to csv started -----------------------

                    # Directory based on env variable
                    type_dir = os.path.join(UPLOAD_DIR, "csv")
                    os.makedirs(type_dir, exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    new_filename = f"{timestamp}_{new_csv_filename}"
                    file_path = os.path.join(type_dir, new_filename)

                    # Prepare log entry
                    log_entry = {
                        "timestamp": timestamp,
                        "original_filename": original_table_name,
                        "stored_as": new_filename,
                        "file_type": "csv",
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
            ## ----------------------------- store log to csv closed ---------------------------

            return file_details

        except Exception as e:
            logger.error("Exception occurred during extraction of URL data.")
            raise CustomException(e, sys)
