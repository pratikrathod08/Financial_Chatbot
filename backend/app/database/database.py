import os, sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from contextlib import contextmanager
from sqlalchemy import inspect
from sqlalchemy import create_engine

from dotenv import load_dotenv
load_dotenv()


DATABASE_URL = os.getenv("DB_URI")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

db = SessionLocal()

@contextmanager
def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_full_schema():
    inspector = inspect(engine)
    schema_details = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema_details[table_name] = [
            {
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": col.get("default"),
                "primary_key": col.get("primary_key")
            }
            for col in columns
        ]
    
    return schema_details