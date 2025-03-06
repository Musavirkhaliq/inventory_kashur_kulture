from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from ..users import services as user_services
from ..config import settings

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
            logger.error("Invalid token payload: No 'sub' claim")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWT decoding error: {str(e)}")
        raise credentials_exception
    
    user = user_services.get_user_by_email(db, email=email)
    if user is None:
        logger.error(f"User not found for email: {email}")
        raise credentials_exception
    return user

async def get_current_verified_user(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_email_verified:
        logger.warning(f"Email not verified for user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please verify your email first."
        )
    return current_user