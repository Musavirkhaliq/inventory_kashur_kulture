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

class SaleBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: int = Field(gt=0)
    selling_price: float = Field(gt=0)
    amount_received: float = Field(ge=0)

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    sale_date: datetime

    class Config:
        from_attributes = True

class RestockBase(BaseModel):
    product_id: int
    quantity: int

class RestockCreate(RestockBase):
    pass

class Restock(RestockBase):
    id: int
    restock_date: datetime
    product_name: str  # Add product name

    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    sale_id: int

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    invoice_date: datetime

    class Config:
        from_attributes = True