# router/openai_router.py
from fastapi import APIRouter
from app.chat import chat

router = APIRouter(
    prefix="/api",  # Base path for all routes in this router
    tags=["v1"] 
)

router.include_router(chat.router)