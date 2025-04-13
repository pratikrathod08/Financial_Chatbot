import os, sys
import csv
import uuid
from datetime import datetime

from app.database.database import get_db_connection
from app.logger import logger 
from app.exception import CustomException
from dotenv import load_dotenv
load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")
CSV_PATH = os.path.join(UPLOAD_DIR, "chat_history.csv")

def log_chat_to_csv(query: str, response: str):
    """
    Logs the chat query and response to a local CSV file with timestamp and unique ID.
    """
    unique_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(CSV_PATH)

    try:
        with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["id", "timestamp", "query", "response"])  # Write header once
            writer.writerow([unique_id, timestamp, query, response])
    except Exception as e:
        print(f"Error while logging chat to CSV: {str(e)}")



def run_sql_query(query: str):
    try:
        logger.info("Run sql query function called") 
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e: 
        logger.info(f"Exception occure during run sql query : {str(e)}")
        raise CustomException(e, sys)


def get_db_schema():
    try : 
        logger.info("Database schema gathering started")
        schema = {}

        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table_name_tuple in tables:
                table_name = table_name_tuple[0]

                # Get column info for each table
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()

                # Extract column name and type
                schema[table_name] = [
                    {"name": col[1], "type": col[2]} for col in columns
                ]

        return schema
    except Exception as e: 
        logger.info("Exception occure during gathering schema of database")
        raise CustomException(e, sys)
