import os, sys
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine
from langchain.agents import initialize_agent, AgentType
from app.tools.sql_tool import SqlTool
from app.database.database import get_db_connection
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(temperature=0, model_name="gpt-4o")  # Or use Bedrock with LangChain
DB_URI=os.getenv("DB_URI")
engine = create_engine(DB_URI)

sql_tool = SqlTool(llm=llm, db_connection=get_db_connection)
sql_generator_tool = sql_tool.sql_generator_tool()
sql_executor_tool = sql_tool.sql_query_executor_tool()

tools = [sql_generator_tool, sql_executor_tool]

agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
    handle_parsing_errors=True
)



# Optional: Example of using the agent
def main():
    try:
        # Example query
        query = "Show me the top 5 customers by total purchase amount"
        response = agent_executor.invoke({"input": query})
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()