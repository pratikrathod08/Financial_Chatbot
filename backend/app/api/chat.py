import os, sys
from fastapi import APIRouter, Request
from langchain_core.messages import ToolMessage, HumanMessage 

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
        return {"result": final_state["messages"][-1].content}
    except Exception as e:
        print(e)
        return {"result": "error"}