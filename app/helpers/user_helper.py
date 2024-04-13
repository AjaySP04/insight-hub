# helpers/user_helper.py
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError


from app.models.user_model import User, UserInDB, UserLogin
from app.models.response_model import ResponseMsg, UserResponseMsg
from app.db.mongo_db import MongoDB
from app.logger.logger import logger
from app.configs import config
from app.configs.constants import UserCollection, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM


async def create_user(user: UserInDB) -> UserInDB:
    # Set the created_time, updated_time to the current datetime
    user.created_time = datetime.now(timezone.utc)
    user.updated_time = datetime.now(timezone.utc)
    user.last_login = datetime.now(timezone.utc)
    user.disabled = False
    
    user_dict = user.model_dump()
    new_user = await MongoDB.insert_one(UserCollection, user_dict)
    user.id = new_user.inserted_id
    return user


async def get_user_by_email(email: str) -> UserInDB | None:
    user = await MongoDB.find_one(UserCollection, {"email": email})
    return user


async def get_user_by_google_user_id(google_user_id: str) -> UserInDB | None:
    user = await MongoDB.find_one(UserCollection, {"google_user_id": google_user_id})
    return user


async def get_existing_user(google_user_id: str, email: Optional[str]) -> UserInDB | None:
    if email != "" and email is not None:
        existing_user = await get_user_by_email(email)
    else:
        existing_user = await get_user_by_google_user_id(google_user_id)
    return existing_user


async def user_login(user_info: UserLogin) -> UserResponseMsg:
    response = UserResponseMsg()

    existing_user: UserInDB | None = await get_existing_user(user_info.google_user_id, email=user_info.email)
    if existing_user is None:
        new_user: UserInDB = UserInDB(
            google_user_id=user_info.google_user_id,
            email=user_info.email,
            name=user_info.name,
            full_name=user_info.full_name,
            profile_picture_url=user_info.profile_picture_url,
            oauth2_token=user_info.oauth2_token,
            refresh_token=user_info.refresh_token
        )
        user: UserInDB = await create_user(new_user)
        if user.id:
            response.user = user
            response.message = "User created successfully"
        else:
            response.error = "Failed to create user"
    else:
        if isinstance(existing_user, dict):
            existing_user = UserInDB(**existing_user)
        
        existing_user.disabled = False
        existing_user.oauth2_token = user_info.oauth2_token
        existing_user.refresh_token = user_info.refresh_token
        existing_user.last_login = datetime.now(timezone.utc)
        user_dict = existing_user.model_dump()
        result = await MongoDB.update_one(UserCollection, {"google_user_id": existing_user.google_user_id}, user_dict)
        if result.modified_count == 1:
            response.user = existing_user
            response.message = "User information updated successfully"
        else:
            response.error  = "Failed to update user information"
    return response


async def user_logout(google_user_id: str, email: str = "") -> ResponseMsg:
    response = ResponseMsg()

    if email != "":
        existing_user = await get_user_by_email(email)
    else:
        existing_user = await get_user_by_google_user_id(google_user_id)

    if existing_user is None:
        response.error = f"User not found for email - {email} and user_id - {google_user_id}"
        return response

    # Update the existing user data with the new data
    existing_user.disabled = True
    existing_user.oauth2_token = None
    existing_user.refresh_token =  None
    user_dict = existing_user.model_dump()
    result = await MongoDB.update_one(UserCollection, {"email": email}, user_dict)
    if result.modified_count == 1:
        response.message = "User logout successful"
    else:
        response.error  = "Failed to logout user"
    return response
