import os, sys
from fastapi import APIRouter, Request
from langchain_core.messages import ToolMessage, HumanMessage 

from app.schemas.chat_schema import AskRequest
from app.agent.agent_graph import graph, config
from app.agent.openai_agent import agent
from app.logger import logger 
from app.exception import CustomException
from app.models.models import ChatHistory
from app.database.database import SessionLocal
from app.utils.chat_utils import log_chat_to_csv


from dotenv import load_dotenv
load_dotenv()


router = APIRouter()

@router.post("/ask/")
async def ask_files(request: AskRequest):
    db = SessionLocal()
    try:
        logger.info("Get a user query for agent call")
        final_state = graph.invoke(
            {"messages": [HumanMessage(content=request.query)]},
            config=config
        )
        response_text = final_state["messages"][-1].content

        # response_text = agent.run(request.query)
        logger.info(f"Answer of user query : {response_text}")

        # ✅ Log to CSV
        log_chat_to_csv(request.query, response_text)

        logger.info(f"Answer of user query : {response_text}")
        return {"result": response_text}
    
    except Exception as e:
        logger.info(f"Exception occure during user query response : {str(e)}")
        return {"result": "Error during response"}