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

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "mongodb")
DATABASE_URL = os.getenv("DATABASE_URL", "")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "insight_hub_db")
DATABASE_USER = os.getenv("DATABASE_USER", "admin")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
