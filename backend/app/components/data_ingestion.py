import os, sys
import csv
from datetime import datetime
import sqlite3
import pandas as pd
from sqlalchemy import inspect

from app.components.data_extraction import DataExtractor
from app.components.vectorstore import VectorStore
from app.database.database import get_db_connection, engine
from app.logger import logger
from app.exception import CustomException

from dotenv import load_dotenv
load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")
LOG_PATH = os.path.join(UPLOAD_DIR, "ingestion_log.csv")

def table_exists(table_name: str) -> bool:
    inspector = inspect(engine)
    return inspector.has_table(table_name)

def log_ingestion_event(storage_type: str, filename: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(LOG_PATH)

    with open(LOG_PATH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "filename", "storage"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": timestamp,
            "filename": filename,
            "storage": storage_type
        })


class DataIngestion:

    def __init__(self):
        logger.info("Data ingestion started")
        self.data_extractor = DataExtractor()
        self.vectorstore = VectorStore()

    def store_csv_excel_to_sqlite(self, df, table_name: str):
        try: 
            logger.info("Request get for store csv to database") 
            if table_exists(table_name):
                logger.info("Table already available in database")    
            else: 
                df.to_sql(table_name, engine, if_exists="replace", index=False, method='multi')
                logger.info("Stored csv or excel successfully")
        except Exception as e: 
            logger.info(f"Exception occure during store file to database : {str(e)}")
            raise CustomException(e, sys)

    def data_ingestion(self, filedata: dict):
        filetype = filedata.get("file_type") 
        filepath = filedata.get("path")
        filename = filedata.get("original_filename")

        if filetype in ["txt", "docx", "pdf"]:
            try: 
                text= self.data_extractor.extract_text(filepath)
                self.vectorstore.add_to_vectorstore(text, filename)
                logger.info("pdf, docx, txt ingestion completed")
                log_ingestion_event("Vector Database", filename)
            except Exception as e:
                logger.info(f"Exception during store file {filename}") 
                raise CustomException(e, sys)

        elif filetype in ['xlsx', "csv"]:
            try: 
                df= self.data_extractor.extract_df(filepath)
                print("DataFrame : ", df.head())
                self.store_csv_excel_to_sqlite(df, filename.split(".")[0])
                logger.info("csv and excel ingestion completed")
                log_ingestion_event("SQL Database", filename)
            except Exception as e: 
                logger.info(f"Exception during store file {filename}")
                raise CustomException(e, sys)

        else:
            logger.warning(f"Unsupported file type: {filetype}")
            raise CustomException(f"Unsupported file type: {filetype}", sys)
