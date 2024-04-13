# models/user_model.py
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Any, Dict

from app.models import PyObjectId


class Email(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    google_user_id: Optional[str] | None = None
    email: Optional[EmailStr] | None = None

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v) if v else None,  # Custom JSON encoder for ObjectId
            PyObjectId: lambda v: str(v) if v else None,  # Custom JSON encoder for PyObjectId
            datetime: lambda v: v.isoformat() if v else None,
        }
        json_schema_extra = {
            "example": {
                "name": "jane_doe",
                "google_user_id": "3213424234",
                "email": "jdoe@example.com",
            }
        }


class EmailInDB(Email):
    pass


class PaginatedEmailListResponse(BaseModel):
    count: int
    limit: int
    skip: int
    emails: List[Any]

class EmailListResponse(BaseModel):
    count: int
    emails: Dict[Any, Any]
