from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

from app.agent.sql_tool import query_sqldb 
from app.agent.vector_tool import lookup_vectordb

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = [lookup_vectordb, query_sqldb]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

response = agent.run("give me average age of car buyers")
print(response)
