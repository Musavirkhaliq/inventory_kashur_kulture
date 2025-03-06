from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from app.database import get_db
from app.users.services import send_verification_email, get_user_by_email, verify_otp, create_email_verification
from ..config import settings
from app.auth.services import create_access_token, verify_password
import time
import logging

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="frontend/templates")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Rate limiting storage
verification_attempts = {}  # {email: [(timestamp, attempt_count)]}

def check_rate_limit(email: str) -> bool:
    now = time.time()
    hour_ago = now - 3600
    if email in verification_attempts:
        verification_attempts[email] = [
            (ts, count) for ts, count in verification_attempts[email] if ts > hour_ago
        ]
    attempts = verification_attempts.get(email, [])
    recent_attempts = sum(count for ts, count in attempts)
    return recent_attempts < 3

def add_verification_attempt(email: str):
    now = time.time()
    if email not in verification_attempts:
        verification_attempts[email] = []
    verification_attempts[email].append((now, 1))

@router.post("/send-verification")
async def send_verification(email: str = Query(...), db: Session = Depends(get_db)):
    logger.debug(f"Sending verification for email: {email}")
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not check_rate_limit(email):
        raise HTTPException(status_code=429, detail="Too many verification attempts. Please try again in an hour.")
    
    verification = create_email_verification(db, email)
    success = await send_verification_email(email=email, name=email.split("@")[0], otp=verification.otp)
    if not success:
        logger.error(f"Failed to send verification email to: {email}")
        raise HTTPException(status_code=500, detail="Failed to send verification email")
    
    add_verification_attempt(email)
    return {"message": "Verification email sent"}

@router.post("/verify-otp")
async def verify_otp_endpoint(email: str = Form(...), otp: str = Form(...), db: Session = Depends(get_db)):
    logger.debug(f"Verifying OTP for email: {email}")
    if verify_otp(db, email, otp):
        user = get_user_by_email(db, email=email)
        if not user:
            logger.error(f"User not found during OTP verification for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        try:
            access_token = create_access_token(
                data={"sub": email},
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            user.is_email_verified = True
            db.commit()
            logger.debug(f"Email verified and token generated for: {email}")
            return {"message": "Email verified successfully", "access_token": access_token, "token_type": "bearer"}
        except Exception as e:
            logger.error(f"Failed to generate access token during OTP verification for {email}: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate access token after verification")
    logger.error(f"Invalid or expired OTP for email: {email}")
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

@router.get('/login/google')
async def google_login(request: Request):
    logger.debug("Initiating Google OAuth login")
    try:
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        return await oauth.google.authorize_redirect(request, redirect_uri, access_type='offline')
    except Exception as e:
        logger.error(f"Google OAuth init failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Google OAuth init failed: {str(e)}")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.debug(f"Login attempt for username: {form_data.username}")
    user = get_user_by_email(db, email=form_data.username)
    if not user:
        logger.error(f"User not found for email: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, user.hashed_password):
        logger.error(f"Invalid password for user: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_email_verified:
        logger.warning(f"Email not verified for user: {form_data.username}")
        return JSONResponse(content={"message": "verify_email", "email": user.email}, status_code=200)
    
    try:
        access_token = create_access_token(
            data={"sub": user.email, "username": user.username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        logger.debug(f"Access token generated for user: {user.email}")
        # return {"access_token": access_token, "token_type": "bearer"}
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "username": user.username,
                "is_email_verified": user.is_email_verified,
                "created_at": user.created_at.isoformat(),  # Convert DateTime to string
            }
        }   
    except Exception as e:
        logger.error(f"Failed to create access token for user {user.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate access token")

@router.get('/callback')
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    logger.debug("Processing Google OAuth callback")
    try:
        google_user = await oauth.get_google_oauth_token(request)
        user = await oauth.get_or_create_user_from_google(db, google_user)
        access_token = create_access_token(
            data={"sub": user.email, "username": user.username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        logger.debug(f"Google OAuth successful for user: {user.email}")
        return templates.TemplateResponse(
            "callback.html",
            {
                "request": request,
                "access_token": access_token,
                "token_type": "bearer",
                "redirect_url": "/admin"
            },
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error during Google authentication: {str(e)}")
        return templates.TemplateResponse(
            "callback.html",
            {"request": request, "detail": str(e)},
            status_code=400
        )