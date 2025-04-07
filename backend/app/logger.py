# app/logger.py
import logging
import os
from datetime import datetime

# Logs directory
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
logs_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(logs_dir, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Create a custom logger
logger = logging.getLogger("financial_chatbot")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers on multiple imports
if not logger.handlers:
    # File handler
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s'))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s'))

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
