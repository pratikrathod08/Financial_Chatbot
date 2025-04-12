import os ,sys
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import tool
from operator import itemgetter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from operator import itemgetter
load_dotenv()

# sql_uri= os.getenv("DB_URI")
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API')

# sql_llm = ChatOpenAI(model="gpt-4o", temperature=0 )

# system_role = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.\n
#     Question: {question}\n
#     SQL Query: {query}\n
#     SQL Result: {result}\n
#     Answer:
#     """
# db = SQLDatabase.from_uri(sql_uri)

# execute_query = QuerySQLDataBaseTool(db=db)
# write_query = create_sql_query_chain(
#     sql_llm, db)
# answer_prompt = PromptTemplate.from_template(
#     system_role)


# answer = answer_prompt | sql_llm | StrOutputParser()
# chain = (
#     RunnablePassthrough.assign(query=write_query).assign(
#         result=itemgetter("query") | execute_query
#     )
#     | answer
# )
# # Test the chain
# # message = "How many tables do I have in the database? and what are their names?"
# # response = chain.invoke({"question": message})

# @tool
# def query_sqldb(query):
#     """Query the SQL Database and access all the information. Input should be a search query."""
#     response = chain.invoke({"question": query})
#     return response


## Travel sql agent tool design 


# TOOLS_CFG = LoadToolsConfig()
sql_agent_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
sql_uri = os.getenv("DB_URI")
sql_llm_temperature = 0

class TravelSQLAgentTool:
    """
    A tool for interacting with a travel-related SQL database using an LLM (Language Model) to generate and execute SQL queries.

    This tool enables users to ask travel-related questions, which are transformed into SQL queries by a language model.
    The SQL queries are executed on the provided SQLite database, and the results are processed by the language model to
    generate a final answer for the user.

    Attributes:
        sql_agent_llm (ChatOpenAI): An instance of a ChatOpenAI language model used to generate and process SQL queries.
        system_role (str): A system prompt template that guides the language model in answering user questions based on SQL query results.
        db (SQLDatabase): An instance of the SQL database used to execute queries.
        chain (RunnablePassthrough): A chain of operations that creates SQL queries, executes them, and generates a response.

    Methods:
        __init__: Initializes the TravelSQLAgentTool by setting up the language model, SQL database, and query-answering pipeline.
    """

    def __init__(self, llm: str, sql_uri: str, llm_temerature: float) -> None:
        """
        Initializes the TravelSQLAgentTool with the necessary configurations.

        Args:
            llm (str): The name of the language model to be used for generating and interpreting SQL queries.
            sqldb_directory (str): The directory path where the SQLite database is stored.
            llm_temerature (float): The temperature setting for the language model, controlling response randomness.
        """
        self.sql_agent_llm = ChatOpenAI(
            model=llm, temperature=llm_temerature)
        self.system_role = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.\n
            Question: {question}\n
            SQL Query: {query}\n
            SQL Result: {result}\n
            Answer:
            """
        self.db = SQLDatabase.from_uri(sql_uri)
        print(self.db.get_usable_table_names())

        execute_query = QuerySQLDataBaseTool(db=self.db)
        write_query = create_sql_query_chain(
            self.sql_agent_llm, self.db)
        answer_prompt = PromptTemplate.from_template(
            self.system_role)

        answer = answer_prompt | self.sql_agent_llm | StrOutputParser()
        self.chain = (
            RunnablePassthrough.assign(query=write_query).assign(
                result=itemgetter("query") | execute_query
            )
            | answer
        )

@tool
def query_sqldb(query: str) -> str:
    """Query the Swiss Airline SQL Database and access all the company's information. Input should be a search query."""
    agent = TravelSQLAgentTool(
        llm=sql_agent_llm,
        sqldb_directory=sql_uri,
        llm_temerature=sql_llm_temperature
    )
    response = agent.chain.invoke({"question": query})
    return response
