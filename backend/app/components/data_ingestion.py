import os, sys
import sqlite3
import pandas as pd
from app.components.data_extraction import DataExtractor
from app.components.vectorstore import VectorStore
from app.database.database import get_db_connection, engine

from app.logger import logger

# data_extractor = DataExtractor()

# {
#         "original_filename": filename,
#         "stored_as": new_filename,
#         "file_type": file_type,
#         "path": file_path
#     }

# class DataIngestion(DataExtractor, VectorStore):
#     def __init__(self):
#         logger.info("Data ingestion started")
#         self.data_extractor=DataExtractor()
#         self.vectorstore=VectorStore()

#     def store_csv_excel_to_sqlite(self, df: pd.DataFrame, table_name: str):
#         with get_db_connection() as conn:
#             df.to_sql(table_name, conn, if_exists="replace", index=False)
#             logger.info("Stored csv or excel successfully")
            

#     def data_ingestion(self, filedata: dict):
#         filetype = filedata.get("file_type") 
#         filepath = filedata.get("path")
#         filename = filedata.get("original_filename")
#         if filetype in ["txt", "docx", "pdf"]:
#             text = self.data_extractor.extract_text(filepath)
#             result = self.vectorstore.add_to_vectorstore(text, filename)
#             logger.info("pdf, docx, txt ingestion completed")
        
#         elif filetype in ['xlsx', "csv"]:
#             df = self.data_extractor.extract_df(filepath)
#             result = self.store_csv_excel_to_sqlite(df, filename.split(".")[0])
#             logger.info("csv and excel ingestion completed")
            

# def run_sql_query(query: str, db_path="data.db"):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute(query)
#     result = cursor.fetchall()
#     conn.close()
#     return result

# llm_generated_sql = generate_sql_from_prompt(user_input, table_schema)

# answer = run_sql_query(llm_generated_sql)


class DataIngestion:

    def __init__(self):
        logger.info("Data ingestion started")
        self.data_extractor = DataExtractor()
        self.vectorstore = VectorStore()

    # def store_csv_excel_to_sqlite(self, df, table_name: str):
    #     with get_db_connection() as conn:
    #         df.to_sql(table_name, conn, if_exists="replace", index=False)
    #         logger.info("Stored csv or excel successfully")

    def store_csv_excel_to_sqlite(self, df, table_name: str):
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        logger.info("Stored csv or excel successfully")

    def data_ingestion(self, filedata: dict):
        filetype = filedata.get("file_type") 
        filepath = filedata.get("path")
        filename = filedata.get("original_filename")

        if filetype in ["txt", "docx", "pdf"]:
            text = self.data_extractor.extract_text(filepath)
            self.vectorstore.add_to_vectorstore(text, filename)
            logger.info("pdf, docx, txt ingestion completed")

        elif filetype in ['xlsx', "csv"]:
            df = self.data_extractor.extract_df(filepath)
            print("DataFrame : ", df.head())
            self.store_csv_excel_to_sqlite(df, filename.split(".")[0])
            logger.info("csv and excel ingestion completed")

        else:
            logger.warning(f"Unsupported file type: {filetype}")
            raise ValueError("Unsupported file type")
