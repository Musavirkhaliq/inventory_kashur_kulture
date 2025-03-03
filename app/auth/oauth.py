from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from fastapi import HTTPException
import httpx
from sqlalchemy.orm import Session
from ..config import settings
from ..users import services as user_services, schemas
import secrets

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=settings.GOOGLE_CONF_URL,
    client_kwargs={'scope': 'openid email profile', 'prompt': 'select_account'},
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_params={'access_type': 'offline'}
)

async def google_oauth_init(request: Request):
    try:
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        return await oauth.google.authorize_redirect(request, redirect_uri, access_type='offline')
    except Exception as e:
        print(f"Error in google_oauth_init: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Google OAuth init failed: {str(e)}")

async def get_google_oauth_token(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        if not token:
            raise HTTPException(status_code=400, detail="No token received from Google")
        
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {token["access_token"]}'}
            response = await client.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info from Google")
            user_info = response.json()
            if not user_info or 'email' not in user_info:
                raise HTTPException(status_code=400, detail="Invalid user info from Google")
            return user_info
    except Exception as e:
        print(f"Error in get_google_oauth_token: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

async def get_or_create_user_from_google(db: Session, google_user: dict):
    email = google_user.get('email')
    if not email:
        raise HTTPException(status_code=400, detail="Invalid Google user data")
    
    user = user_services.get_user_by_email(db, email=email)
    if not user:
        random_pass = secrets.token_urlsafe(32)
        username = email.split('@')[0]
        user_create = schemas.UserCreate(email=email, password=random_pass, username=username)
        user = user_services.create_user(db=db, user=user_create)
        user.is_email_verified = True  # Google users are pre-verified
        db.commit()
    return user