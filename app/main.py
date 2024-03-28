# app/main.py
from fastapi import FastAPI, status
from app.configs import config
from app.logger.logger import logger

app = FastAPI()

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
