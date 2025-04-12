import os, sys
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from contextlib import contextmanager
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

# DB_PATH = os.getenv("DB_PATH")  # You can also use a full path if needed

# # Context manager for SQLite connection
# @contextmanager
# def get_db_connection():
#     conn = sqlite3.connect(DB_PATH)
#     try:
#         yield conn
#     finally:
#         conn.close()


# DATABASE_URL = "postgresql://postgres:Pratik008@localhost/test"

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# mysql_url = "mysql+pymysql://root:my_password@localhost:3306/my_database"
DATABASE_URL = os.getenv("DB_URI")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)


Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Dependency
@contextmanager
def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import inspect

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