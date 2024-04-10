# user/user.py
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from app.models.user_model import User, PaginatedUserResponse
from app.db.mongo_db import MongoDB
from app.configs.constants import UserCollection

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(user: User):
    # Set the created_time, updated_time to the current datetime
    user.created_time = datetime.now(timezone.utc)
    user.updated_time = datetime.now(timezone.utc)
    user.last_login = None
    
    user_dict = user.dict()
    new_user = await MongoDB.insert_one(UserCollection, user_dict)
    user.id = new_user.inserted_id
    return user


@router.get("/users/count", response_model=int)
async def count_users():
    count = await MongoDB.count_documents(UserCollection, {})
    return count


@router.get("/users/", response_model=PaginatedUserResponse)
async def list_users(limit: int = 10, skip: int = 0, sort: Optional[str] = None):
    users = await MongoDB.find(UserCollection, {}, limit, skip, sort)
    total_count = await MongoDB.count_documents(UserCollection, {})

    return PaginatedUserResponse(
        count=total_count,
        limit=limit,
        skip=skip,
        users=users
    )


@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str):
    try:
        object_id = ObjectId(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user_id, error: {e}")

    user = await MongoDB.find_one(UserCollection, {"_id": object_id})
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_data: User):
    try:
        object_id = ObjectId(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Invalid user_id: {e}")

    existing_user = await MongoDB.find_one(UserCollection, {"_id": object_id})
    if existing_user:
        # Update the existing user data with the new data
        existing_user.update(user_data.dict(exclude_unset=True))
        existing_user["updated_time"] = datetime.now(timezone.utc)
        updated_user = await MongoDB.update_one(UserCollection, {"_id": object_id}, existing_user)

        if updated_user:
            return existing_user 
        else:
            raise HTTPException(status_code=500, detail="Failed to update user")
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    try:
        object_id = ObjectId(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user_id, error: {e}")

    result = await MongoDB.delete_one(UserCollection, {"_id": object_id})
    if result.deleted_count == 1:
        return {"message": f"User {user_id} deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
