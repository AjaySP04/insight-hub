# app/configs/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application Constants
PROJECT_NAME = os.getenv("PROJECT_NAME", "InsightHub Test")
PROJECT_DESC = os.getenv("PROJECT_DESCRIPTION", "InsightHub Project description")
HOST = os.getenv("APP_HOST", "localhost")
PORT = int(os.getenv("APP_PORT", 8000))
API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
