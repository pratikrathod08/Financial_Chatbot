# app/main.py
from fastapi import FastAPI
import uvicorn
from app.api import chat, file  # you'll create __init__.py in `api/` to collect routers
from app.logger import logger

app = FastAPI(
    title="Financial Intelligence Chatbot",
    version="1.0.0"
)
logger.info("Started application loggind")
app.include_router(chat.router, prefix="/chat", tags=['files'])
app.include_router(file.router, prefix="/file", tags=['Queries'])

if __name__ == "__main__":
    uvicorn.run(app)
