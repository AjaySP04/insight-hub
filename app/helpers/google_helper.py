# helpers/google_helper.py
from fastapi import HTTPException, Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.configs import config


async def get_authenticated_google_service(service_name: str, version: str, access_token: str, refresh_token: str  = ""):
    credentials = Credentials(
        account=None,
        client_id=config.GOOGLE_CLIENT_ID,
        client_secret=config.GOOGLE_CLIENT_SECRET,
        token=access_token,
        refresh_token=refresh_token
    )
    service = build(service_name, version, credentials=credentials)
    return service


async def get_gmail_service(access_token: str):
    return await get_authenticated_google_service("gmail", "v1", access_token)


async def get_user_info_service(access_token: str):
    return await get_authenticated_google_service("oauth2", "v2", access_token)


async def get_calendar_service(access_token: str):
    return await get_authenticated_google_service("calendar", "v3", access_token)


async def get_drive_service(access_token: str):
    return await get_authenticated_google_service("drive", "v3", access_token)


async def get_access_token(request: Request):
    session_data = request.session.get('user')
    if session_data is None or 'token' not in session_data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return session_data['token']
