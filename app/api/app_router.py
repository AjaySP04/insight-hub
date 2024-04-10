# router/openai_router.py
from fastapi import APIRouter
from app.api.chat import chat
from app.api.user import user

router = APIRouter(
    prefix="/api",  # Base path for all routes in this router
    tags=["v1"] 
)

router.include_router(chat.router)
router.include_router(user.router)
