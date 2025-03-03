from fastapi import APIRouter, Request, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from app.utils.utils import render_template
from .users import services as user_services
from .database import get_db

from sqlalchemy.orm import Session

router = APIRouter(tags=["web"])

templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def read_login(request: Request, error: Optional[str] = Query(None)):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@router.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/verify-email", response_class=HTMLResponse)
async def read_verify_email(
    request: Request,
    email: str,
    db: Session = Depends(get_db)
):
    # Check if the user exists and is not verified
    user = user_services.get_user_by_email(db, email=email)
    if not user:
        return RedirectResponse(url="/register")
    if user.is_email_verified:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("verify_email.html", {"request": request, "email": email})