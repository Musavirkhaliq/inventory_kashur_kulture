from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(gt=0)
    quantity: Optional[int] = Field(ge=0)

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    balance_owe: float = Field(default=0.0, ge=0)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)

class SaleItemCreate(SaleItemBase):
    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

class SaleItem(SaleItemBase):
    id: int
    sale_id: int

    class Config:
        from_attributes = True

class SaleCreate(BaseModel):
    customer_id: int
    items: List[SaleItemCreate]
    amount_received: float = Field(ge=0)

    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('Sale must have at least one item')
        return v

class Sale(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    amount_received: float
    balance: float
    sale_date: datetime
    status: str
    items: List[SaleItem]

    class Config:
        from_attributes = True

class RestockCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class Restock(RestockCreate):
    id: int
    restock_date: datetime
    product_name: str

    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    sale_id: int

class Invoice(InvoiceCreate):
    id: int
    invoice_date: datetime

    class Config:
        from_attributes = True




class PaymentBase(BaseModel):
    amount: float
    method: str
    reference: Optional[str] = None
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    customer_id: int
    date: datetime

class PaymentResponse(PaymentBase):
    id: int
    customer_id: int
    date: datetime

    class Config:
        from_attributes = True

# class CustomerBase(BaseModel):
#     name: str
#     email: str
#     phone_number: str
#     address: str
#     balance_owe: float

class CustomerResponse(CustomerBase):
    id: int
    last_payment_date: Optional[datetime] = None
    payment_count: int = 0
    payments: List[PaymentResponse] = []

    class Config:
        from_attributes = True