from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

import requests
from app.configs import config, constants
from app.logger.logger import logger
from app.models.user_model import UserLogin, User
from app.helpers import user_helper, google_helper


SCOPES: list[str] = [
    'https://www.googleapis.com/auth/userinfo.profile',
    # 'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]


oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    client_kwargs={
        'scope': " ".join(SCOPES),
        'redirect_uri': config.GOOGLE_REDIRECT_URI,
        'access_type': 'offline',
        'include_granted_scopes': 'false',
        'prompt': 'consent',
    }
)

router = APIRouter()

@router.get("/auth/google")
async def google_authentication(request: Request):
    rv = await oauth.google.create_authorization_url(config.GOOGLE_REDIRECT_URI)
    await oauth.google.save_authorize_data(request, redirect_uri=config.GOOGLE_REDIRECT_URI, **rv)
    return {"authorization_url": rv['url']} 


@router.get("/auth/google/callback")
async def google_authentication_callback(code: str, request: Request):
    try:
        response = requests.post(constants.GOOGLE_TOKEN_URI, data={
            "code": code,
            "client_id": config.GOOGLE_CLIENT_ID,
            "client_secret": config.GOOGLE_CLIENT_SECRET,
            "redirect_uri": config.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
            "access_type": "offline"
        })
        response_json = response.json()
        logger.info(f"response_json - {response_json}")
        access_token = response_json.get("access_token")
        refresh_token = response_json.get("refresh_token")

        user_info = requests.get(constants.GOOGLE_AUTH_USER_INFO, headers={"Authorization": f"Bearer {access_token}"})
        if user_info is None:
            raise HTTPException(status_code=401, detail="Invalid access token or code")
        
        user_data = user_info.json()

        user_login_data = UserLogin(
            google_user_id=user_data.get("id"),
            email=user_data.get("email"),
            name=user_data.get("given_name"),
            full_name=user_data.get("name"),
            profile_picture_url=user_data.get("picture"),
            oauth2_token=access_token,
            refresh_token=refresh_token
        )
        result = await user_helper.user_login(user_login_data)
        if result.error != "":
            raise HTTPException(status_code=401, detail=f"error login in user - {result.error}")
        
        if result.user is None:
            raise HTTPException(status_code=401, detail=f"error login in user - {result.error}")
        
        # Store user and access token into session 
        user_data["token"] = access_token
        request.session['user'] = user_data
        logger.info(f" request.session['user'] - > {request.session['user']}")

    except OAuthError as err:
        logger.error(f"oauth error occuured - {err}")
        raise HTTPException(status_code=401, detail="User not authenticated due to oauth error")
    
    except Exception as err:
        logger.error(f"oauth error occuured - {err}")
        raise HTTPException(status_code=401, detail="User not authenticated due to technical error")
    
    logger.info(f"Authentication successful for {result.user.name}")
    redirect_frontend_url = f"{config.FRONTEND_URL}"
    logger.info(f"redirect_frontend_url ->  {redirect_frontend_url}")
    return RedirectResponse(redirect_frontend_url)


@router.get("/user/me", response_model=User)
async def get_current_user(token: str = Depends(google_helper.get_access_token)):
    user_info = requests.get(constants.GOOGLE_AUTH_USER_INFO, headers={"Authorization": f"Bearer {token}"})
    if user_info is None:
        raise HTTPException(status_code=401, detail="Invalid access token or code")
    
    user_data = user_info.json()
    user = await user_helper.get_user_by_google_user_id(user_data.get("id"))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
