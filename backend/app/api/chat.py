import os, sys
from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
import pandas as pd
from langchain_core.messages import ToolMessage, HumanMessage 
import mimetypes
import PyPDF2
import docx

# from app.components.agent import agent_executor
# from app.components.langgraph_agent import graph
from app.schemas.chat_schema import AskRequest
from app.agent.agent_graph import graph, config

from dotenv import load_dotenv
load_dotenv()


router = APIRouter()

@router.post("/ask/")
async def ask_files(request: AskRequest):
    try: 
        print("Request get for chat ")
        # response = agent_executor.invoke({"input": request.query})
        final_state = graph.invoke(
            {"messages": [HumanMessage(content=request.query)]},
            config=config
        )
        # print(final_state)
        print("Final result of query : ", final_state["messages"][-1].content)
        return {"result": final_state["messages"][-1].content}
    except Exception as e:
        print(e)
        return {"result": "error"}