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


sql_agent_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
sql_uri = os.getenv("DB_URI")
sql_llm_temperature = 0

class TravelSQLAgentTool:
    def __init__(self, llm: str, sql_uri: str, llm_temerature: float) -> None:
        self.sql_agent_llm = ChatOpenAI(
            model=llm, temperature=llm_temerature)
        self.system_role = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.\n
            Question: {question}\n
            SQL Query: {query}\n
            SQL Result: {result}\n
            Answer:
            """
        self.db = SQLDatabase.from_uri(sql_uri)

        execute_query = QuerySQLDataBaseTool(db=self.db)
        write_query = create_sql_query_chain(
            llm=self.sql_agent_llm,
            db=self.db
            )
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
        llm='gpt-3.5-turbo',
        sql_uri=sql_uri,
        llm_temerature=sql_llm_temperature
    )
    response = agent.chain.invoke({"question": query})
    return response
