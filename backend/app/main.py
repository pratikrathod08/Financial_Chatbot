import os 
from fastapi import FastAPI
import uvicorn
from app.api import chat, file  # you'll create __init__.py in `api/` to collect routers
from app.logger import logger
from dotenv import load_dotenv


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


app = FastAPI(
    title="Financial Intelligence Chatbot",
    version="1.0.0"
)
logger.info("Application Started")

app.include_router(chat.router, prefix="/chat", tags=['files'])
app.include_router(file.router, prefix="/file", tags=['Queries'])

if __name__ == "__main__":
    uvicorn.run(app)
