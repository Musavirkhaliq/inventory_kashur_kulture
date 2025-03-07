from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    # Core identity fields
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Personal information
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)
    
    # Address information
    shipping_address = Column(String, nullable=True)
    shipping_city = Column(String, nullable=True)
    shipping_state = Column(String, nullable=True)
    shipping_country = Column(String, nullable=True)
    shipping_postal_code = Column(String, nullable=True)
    
    billing_address = Column(String, nullable=True)
    billing_city = Column(String, nullable=True)
    billing_state = Column(String, nullable=True)
    billing_country = Column(String, nullable=True)
    billing_postal_code = Column(String, nullable=True)
    
    # Account status and verification
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    account_type = Column(String, default="customer")  # customer, admin, vendor, etc.
    
    # Security and recovery
    password_reset_token = Column(String, nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    
    # E-commerce specific
    default_payment_method = Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True, unique=True)
    account_credit = Column(Float, default=0.0)

    
    # Preferences
    preferred_language = Column(String, default="en")
    currency_preference = Column(String, default="USD")
    timezone = Column(String, default="UTC")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)  # For soft delete