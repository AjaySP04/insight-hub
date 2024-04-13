# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.logger.logger import logger
from app.configs import config
from app.db.mongo_db import MongoDB
from app.api import app_router
from app.auth import google_auth, google


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the database connection
    await MongoDB.connect()
    yield
    # Clean up database resources
    await MongoDB.close()


app = FastAPI(
    title=f"{config.PROJECT_NAME} API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL, "*"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(app_router.router)
app.include_router(google.router)

# Redirect to Swagger documentation on loading the API for demo purposes
@app.get("/", include_in_schema=False)
def redirect_to_swagger():
    return RedirectResponse(url="/docs")


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    logger.info("Health check status for insight hub backend")
    return {
        "service_name": f"{config.PROJECT_NAME}",
        "service_host": f"{config.HOST}",
        "service_port": f"{config.PORT}",
        "message": f"{config.PROJECT_NAME} Service is healthy and running",
        "title": f"{config.PROJECT_NAME}",
        "description": f"{config.PROJECT_DESC}",
    }
