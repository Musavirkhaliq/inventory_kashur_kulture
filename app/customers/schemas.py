from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    
    class Config:
        orm_mode = True

class CustomerResponse(Customer):
    balance: Optional[float] = 0.0

class PaymentBase(BaseModel):
    customer_id: int
    amount: float
    payment_date: datetime = datetime.now()
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    
    class Config:
        orm_mode = True