from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.utils.utils import render_frontend_template
from ..database import get_db
from . import services
from . import schemas
from app.auth.dependencies import get_current_user

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile", response_model=None)
def read_user_details(
    request: Request,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_user)  # Uncommented for auth
):
    user = services.get_user_by_email(db, email="sartajashraf842@gmail.com")  # Use current_user instead of hardcoded email
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return render_frontend_template("user_profile.html", request, {"profile": user})

@router.put("/update-profile", response_model=schemas.User)
def update_user_profile(
    update_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_user)
):
    user = services.get_user_by_email(db, email="sartajashraf842@gmail.com")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = services.update_user_profile(db, user, update_data)
    return updated_user

@router.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = services.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    return services.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user