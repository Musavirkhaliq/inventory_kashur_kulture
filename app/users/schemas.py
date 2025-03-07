from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    is_email_verified: bool = False

    class Config:
        from_attributes = True 

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_country: Optional[str] = None
    shipping_postal_code: Optional[str] = None
    preferred_language: Optional[str] = None
    currency_preference: Optional[str] = None
    timezone: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True