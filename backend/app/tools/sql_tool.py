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


from app.utils.database_utils import *

class SqlQueryInput(BaseModel):
    query: str = Field(description="SQL query to execute")

class SqlGeneratorInput(BaseModel):
    user_query: str = Field(description="Natural language query to convert to SQL")

class SqlTool:
    def __init__(self, llm, db_connection):
        self.llm = llm
        self.db_connection = db_connection

    def generate_code_using_llm(self, user_query: str, attempt_number=1):
        try:
            # Get table information dynamically
            with self.db_connection() as session:
                tables = session.execute("SHOW TABLES").fetchall()
                table_info = "\n".join([table[0] for table in tables])

            prompt = (
                f"Attempt #{attempt_number}: Given the following tables: {table_info}, "
                f"generate an SQL query suitable for MySQL to answer this: {user_query}. "
                "Make sure the query is syntactically correct and targets the correct table. "
            )
            
            response = self.llm.generate([prompt])
            return response.generations[0][0].text
        except Exception as e:
            return f"Error generating SQL query: {str(e)}"

    def run_sql_query(self, query: str):
        try:
            with self.db_connection() as session:
                result = session.execute(query)
                # Convert results to list of dictionaries
                return [dict(row) for row in result]
        except Exception as e:
            return f"Error executing SQL query: {str(e)}"

    def sql_generator_tool(self):
        return StructuredTool.from_function(
            func=self.generate_code_using_llm,
            name="SqlQueryGenerator",
            description="""
                Advanced SQL Query Generator:
                - Converts natural language to precise SQL queries
                - Understands database schema and relationships
                - Generates complex queries with joins, aggregations
                - Ideal for exploratory data analysis
                """,
            args_schema=SqlGeneratorInput
        )

    def sql_query_executor_tool(self):
        return StructuredTool.from_function(
            func=self.run_sql_query,
            name="SqlQueryExecutor", 
            description="""
                SQL Query Execution Tool:
                - Runs predefined or generated SQL queries
                - Retrieves and processes database results
                - Supports various query types and data retrieval
                - Provides raw data output for further analysis
                """,
            args_schema=SqlQueryInput
        )


## -------------------------------------- old code handwritten --------------------------------

# class SqlTool:
#     def __init__(self, query):
#         self.query = query 
#         self.tables = get_all_tables_and_columns()
#         self.schema = self.tables.get("public")
#         self.llm = ChatOpenAI()


#     # def sql_query_creator(self, tables, q:str):
#     #     table = get_table(tables, q)
#     #     table = table.replace("\\", "").replace("'", "").strip()

#     #     generated_code = generate_code_using_llm(self.schema, q )
#     #     return generated_code
    
#     def generate_code_using_llm(self, attempt_number=1):

#         """ Function for create sql code from schema for get required data """

#         prompt = (
#             f"Attempt #{attempt_number}: Given the following schema: {self.schema}, "
#             f"generate sql query suitable for mysql {self.query}. "

#             "Note : DO not do any mistake in write query understand query and accordingly execute it for table which belongs to it and do not do any mistake"
#             "YOur response should be sql code do not do any mistake in sql query so it give error at the time of execution"
#         )
#         response = self.llm.generate([prompt]) # Pass the prompt as a list
#         return response.generations[0][0].text  # Access the generated text
#         # return generated_code
    
#     # def run_sql_query(query: str):
#     #     with get_db_connection() as session:
#     #         result = session.execute(text(query)).fetchall()
#     #         return result


#     def run_sql_query(self, query: str):
#         with get_db_connection() as session:
#             raw_conn = session.connection().connection  # DBAPI connection
#             cursor = raw_conn.cursor()
#             cursor.execute(query)
#             return cursor.fetchall()
#             # return result


#     def sql_generator_tool(self):
#         return Tool(
#             name="SqlQueryGenerator",
#             func=self.generate_code_using_llm,
#             description="Generate sql query based on given user query and return executable sql code for sqlalchemy engine of fastapi framework where my database is mysql"
#         )
    
#     def sql_query_executor_tool(self):
#         return Tool(
#             name="SqlQueryExecutor", 
#             func=self.run_sql_query, 
#             description="Execute sql query and return result"
#         )
    


    

