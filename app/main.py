# app/main.py
from fastapi import FastAPI, status
from fastapi.openapi.models import OpenAPI, Info
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

from app.configs import config
from app.logger.logger import logger
from app.api.routers import openai_router


app = FastAPI(
    title=f"{config.PROJECT_NAME} API"
)
app.include_router(openai_router.router)

@app.get("/")
def read_root():
    return {"message": f"{config.PROJECT_NAME} service is up and running"}

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    logger.info("Health check status for the application")
    return {
        "service_name": f"{config.PROJECT_NAME}",
        "service_host": f"{config.HOST}",
        "service_port": f"{config.PORT}",
        "message": f"Service is healthy"
    }
