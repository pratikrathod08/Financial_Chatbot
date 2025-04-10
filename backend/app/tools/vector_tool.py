import os, sys 
from langchain_community.utilities import sql_database
from langchain_experimental.utilities import PythonREPL
from langchain.agents import initialize_agent, Tool
from langchain_core import tools
from app.database.database import engine , get_db_connection
from sqlalchemy import text
from langchain_openai import ChatOpenAI

from langchain_core.tools import BaseTool, StructuredTool
from typing import Optional
from pydantic import BaseModel, Field


class VectorQueryInput(BaseModel):
    query: str = Field(description="Vector similarity search query")


class VectorTool:
    def __init__(self) -> None:
        pass
    
