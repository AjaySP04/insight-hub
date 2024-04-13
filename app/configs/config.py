# app/configs/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application Constants
PROJECT_NAME: str = os.getenv("PROJECT_NAME", "InsightHub Test")
PROJECT_DESC: str = os.getenv("PROJECT_DESCRIPTION", "InsightHub Project description")
HOST: str = os.getenv("APP_HOST", "localhost")
PORT = int(os.getenv("APP_PORT", 8000))

FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
FRONTEND_REDIRECT_URL: str = f"{FRONTEND_URL}/"

SECRET_KEY: str = os.getenv("SECRET_KEY", "SECRET API KEY")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "OPENAI API KEY")

GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "GOOGLE CLIENT ID")
GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "GOOGLE CLIENT SECRET")
GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:{PORT}/auth/google/callback")

DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "mongodb")
DATABASE_URL: str = os.getenv("DATABASE_URL", "")
DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", 27017))
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "insight_hub_db")
DATABASE_USER: str = os.getenv("DATABASE_USER", "admin")
DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")
