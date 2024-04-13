# models/user_model.py
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

from app.models import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    google_user_id: Optional[str] | None = None
    name: Optional[str] | None = None
    email: Optional[EmailStr] | None = None
    full_name: Optional[str] | None = None
    profile_picture_url: Optional[str] | None = None
    prompts: List[str] = []
    disabled: bool = False
    last_login: Optional[datetime] = None
    created_time: Optional[datetime] = None
    updated_time: Optional[datetime] = None

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v) if v else None,  # Custom JSON encoder for ObjectId
            PyObjectId: lambda v: str(v) if v else None,  # Custom JSON encoder for PyObjectId
            datetime: lambda v: v.isoformat() if v else None,
        }
        json_schema_extra = {
            "example": {
                "name": "jane_doe",
                "email": "jdoe@example.com",
                "full_name": "Jane Doe",
                "prompts": [],
                "profile_picture_url": None,
                "disabled": None,  # Default to None
                "last_login": None,  # Default to None
                "created_time": None,  # Default to None
                "updated_time": None,  # Default to None
            }
        }


class UserInDB(User):
    oauth2_token: Optional[str] = None
    refresh_token: Optional[str] = None


class UserLogin(BaseModel):
    google_user_id: str
    email: Optional[EmailStr] | None = None
    name: Optional[str] | None = None
    full_name: Optional[str] | None = None
    profile_picture_url: Optional[str] | None = None
    oauth2_token: Optional[str] = None
    refresh_token: Optional[str] = None


class PaginatedUserResponse(BaseModel):
    count: int
    limit: int
    skip: int
    users: List[User]
