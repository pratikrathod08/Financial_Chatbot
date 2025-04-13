import os, sys
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

from app.agent.sql_tool import query_sqldb 
from app.agent.vector_tool import lookup_vectordb
from app.exception import CustomException
from app.logger import logger

llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [lookup_vectordb, query_sqldb]
try: 
    logger.info("Open ai agent building started")    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
except Exception as e:
    logger.info(f"Exception occure during create openai agent : {str(e)}")
    raise CustomException(e, sys)

# response = agent.run("give me average age of car buyers")
# print(response)
