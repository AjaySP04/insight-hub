from typing import Union
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials as OAuth2Credentials
from google.auth.credentials import Credentials as GoogleCredentials
from google.auth.external_account_authorized_user import Credentials as ExternalAccountCredentials
from httplib2 import Credentials

from app.configs import config, constants
from app.models.user_model import UserLogin
from app.helpers import user_helper, google_helper
from app.logger.logger import logger


router = APIRouter()


# If modifying these scopes, delete the file token.json.
SCOPES: list[str] = [
    'https://www.googleapis.com/auth/userinfo.profile',
    # 'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]

CLIENT_CONFIG: dict[str, dict[str, str]] = {
    'web': {
        'client_id': config.GOOGLE_CLIENT_ID,
        'client_secret': config.GOOGLE_CLIENT_SECRET,
        'redirect_uris': config.GOOGLE_REDIRECT_URI,
        'auth_uri': constants.GOOGLE_AUTH_URI,
        'auth_provider_x509_cert_url': constants.GOOGLE_AUTH_PROVIDER_X509_CERT_URI,
        'token_uri': constants.GOOGLE_TOKEN_URI,
        # Or can also use
        # 'token_uri': constants.GOOGLE_TOKEN_URI_V3,
    }
}


# OAuth 2.0 Configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_flow():
    # Initialize the flow using the client ID and secret downloaded earlier.
    flow: Flow = Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=SCOPES
    )
    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required.
    flow.redirect_uri = config.GOOGLE_REDIRECT_URI
    logger.info(f"redirect uri : {config.GOOGLE_REDIRECT_URI}")
    return flow


def redirect_user():
    flow = get_flow()
    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='false',
        # Forces a new refresh token when we authorize the application a second time.
        prompt= "consent"
    )
    return authorization_url, state


@router.get("/auth/google")
async def auth_google():
    authorization_url, state = redirect_user()
    return {"authorization_url": authorization_url}


@router.get("/auth/google/callback")
async def google_auth_callback(code: str):
    flow = get_flow()
    flow.fetch_token(code=code)  # Exchange authorization code for tokens
    credentials = flow.credentials  # Get credentials containing access and refresh tokens
    if credentials is None or credentials.token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZE, detail="User not authenticated")

    user_info_service = await google_helper.get_user_info_service(access_token=credentials.token)
    user_info = user_info_service.userinfo().get().execute()
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZE, detail="Invalid access token or code")
    
    user_login_data = UserLogin(
        google_user_id=user_info.get("id"),
        email=user_info.get("email"),
        name=user_info.get("given_name"),
        full_name=user_info.get("name"),
        profile_picture_url=user_info.get("picture"),
        oauth2_token=credentials.token,
        refresh_token=credentials.refresh_token
    )
    result = await user_helper.user_login(user_login_data)
    if result.error != "":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZE, detail=f"error occured - {result.error}")

    return {
        "message": f"Authentication successful - {result.message}",
        "google_id": user_info.get("id"),
        "email": user_info.get("email"),
        "name": user_info.get("given_name"),
        "access_token": credentials.token
    }
