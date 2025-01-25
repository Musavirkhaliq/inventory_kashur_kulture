# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str
    sku: str
    quantity: int
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_amount: float

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    sale_date: datetime

    class Config:
        orm_mode = True

class InvoiceBase(BaseModel):
    sale_id: int
    customer_name: str

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    invoice_date: datetime

    class Config:
        orm_mode = True

# schemas.py
class SaleCreate(BaseModel):
    product_id: int
    quantity: int
    customer_name: str