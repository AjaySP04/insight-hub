# app/main.py
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from app.logger.logger import logger
from app.configs import config
from app.db.mongo_db import MongoDB
from app.api import app_router


app = FastAPI(
    title=f"{config.PROJECT_NAME} API",
    version="1.0.0",
)

app.include_router(app_router.router)

@app.on_event("startup")
async def startup_event():
    await MongoDB.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await MongoDB.close()

# Redirect to Swagger documentation on loading the API for demo purposes
@app.get("/", include_in_schema=False)
def redirect_to_swagger():
    return RedirectResponse(url="/docs")


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
