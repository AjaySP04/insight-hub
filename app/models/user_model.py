# models/user_model.py
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from app.models import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: Optional[str]
    email: Optional[EmailStr]
    prompts: List[str] = []
    last_login: Optional[datetime] = None
    created_time: Optional[datetime] = None
    updated_time: Optional[datetime] = None

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v) if v else None,  # Custom JSON encoder for ObjectId
            PyObjectId: lambda v: str(v) if v else None,  # Custom JSON encoder for PyObjectId
        }
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "prompts": [],
                "last_login": None,  # Default to None
                "created_time": None,  # Default to None
                "updated_time": None,  # Default to None
            }
        }

class PaginatedUserResponse(BaseModel):
    count: int
    limit: int
    skip: int
    users: List[User]
