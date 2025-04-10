# tools/vector_tool.py
from langchain.tools import Tool
from typing import List

class VectorDBTool:
    def run(self, query: str) -> str:
        # Your vector DB search logic
        # For example:
        # from vector_search import search_vector_db
        # return search_vector_db(query)
        pass

vector_tool = Tool(
    name="VectorDBTool",
    func=VectorDBTool().run,
    description="Use this to search and summarize unstructured documents like PDFs, DOCs."
)

# tools/sql_tool.py
from langchain.tools import Tool

class SQLTool:
    def run(self, query: str) -> str:
        # Your SQL query logic
        # from sql_analytics import run_sql_query
        # return run_sql_query(query)
        pass

sql_tool = Tool(
    name="SQLTool",
    func=SQLTool().run,
    description="Use this tool when the query is related to analytics or database tables."
)

