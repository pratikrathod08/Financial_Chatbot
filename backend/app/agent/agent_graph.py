import os, sys
import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from app.config import ROOT_DIR
from langchain_openai import ChatOpenAI
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage, HumanMessage 
from langgraph.graph import END, MessagesState
from langgraph.checkpoint.memory import MemorySaver

from app.agent.sql_tool import query_sqldb 
from app.agent.vector_tool import lookup_vectordb

from dotenv import load_dotenv
from pprint import pprint
load_dotenv()


tools = [query_sqldb, lookup_vectordb]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key="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")
llm_with_tools = llm.bind_tools(tools)
memory = MemorySaver()

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

def route_tools(
    state: State,
) -> Literal["tools", "__end__"]:
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"

tool_node = BasicToolNode(tools=[query_sqldb, lookup_vectordb])

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", "__end__": "__end__"},
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "1"}}


## Approach 2 

## Define the function that determines whether to continue or not
# def should_continue(state: MessagesState) -> Literal["tools", END]:
#     messages = state['messages']
#     last_message = messages[-1]
#     # If the LLM makes a tool call, then we route to the "tools" node
#     if last_message.tool_calls:
#         return "tools"
#     # Otherwise, we stop (reply to the user)
#     return END

# graph_builder.add_conditional_edges(
#     "chatbot",
#     should_continue,
#     ["tools", END],
# )
# # Any time a tool is called, we return to the chatbot to decide the next step
# graph_builder.add_edge("tools", "chatbot")
# graph_builder.add_edge(START, "chatbot")
# graph = graph_builder.compile(checkpointer=memory)
# config = {"configurable": {"thread_id": "1"}}
