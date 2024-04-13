# models/response_model.py
from pydantic import BaseModel
from app.models.user_model import UserInDB

class ResponseMsg(BaseModel):
    message: str = ""
    error: str = ""


class UserResponseMsg(ResponseMsg):
    user: UserInDB | None = None
