from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form, status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from app.database import get_db
from app.users.services import send_verification_email,get_user_by_email,verify_otp,create_email_verification
from ..config import settings
from app.auth.services import create_access_token,verify_password
from . import oauth
import time

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="frontend/templates")

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

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_email_verified:
        return JSONResponse(content={"message": "verify_email", "email": user.email}, status_code=200)
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/send-verification")
async def send_verification(email: str = Query(...), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not check_rate_limit(email):
        raise HTTPException(status_code=429, detail="Too many verification attempts. Please try again in an hour.")
    
    verification = create_email_verification(db, email)
    success = await send_verification_email(email=email, name=email.split("@")[0], otp=verification.otp)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send verification email")
    
    add_verification_attempt(email)
    return {"message": "Verification email sent"}

@router.post("/verify-otp")
async def verify_otp(email: str = Form(...), otp: str = Form(...), db: Session = Depends(get_db)):
    if verify_otp(db, email, otp):
        access_token = create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"message": "Email verified successfully", "access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

@router.get('/login/google')
async def google_login(request: Request):
    return await oauth.google_oauth_init(request)

@router.get('/callback')
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        google_user = await oauth.get_google_oauth_token(request)
        user = await oauth.get_or_create_user_from_google(db, google_user)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return templates.TemplateResponse(
            "callback.html",
            {"request": request, "access_token": access_token, "token_type": "bearer"}
        )
    except Exception as e:
        import traceback
        print(f"Error during Google authentication: {str(e)}\n{traceback.format_exc()}")
        return templates.TemplateResponse(
            "callback.html",
            {"request": request, "detail": str(e)},
            status_code=400
        )

# Authentication dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = user_services.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_verified_user(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please verify your email first."
        )
    return current_user