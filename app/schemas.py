from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    balance_owe: float = 0.0  # Default is always zero for simplicity
    previous_transactions: List[dict] = []


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True


# Sale Schemas
class SaleBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: int
    selling_price: float  # Price at which the product was sold
    profit: float  # Profit from the sale


class SaleCreate(BaseModel):
    product_id: int
    customer_id: int
    quantity: int
    selling_price: float
    amount_received: float  # New field


class Sale(SaleBase):
    id: int
    sale_date: datetime
    product: Optional[Product] = None
    customer: Optional[Customer] = None

    class Config:
        from_attributes = True


# Restock Schemas
class RestockBase(BaseModel):
    product_id: int
    quantity: int


class RestockCreate(RestockBase):
    pass


class Restock(RestockBase):
    id: int
    restock_date: datetime

    class Config:
        from_attributes = True


# Invoice Schemas
class InvoiceBase(BaseModel):
    sale_id: int


class InvoiceCreate(InvoiceBase):
    pass


class Invoice(InvoiceBase):
    id: int
    invoice_date: datetime

    class Config:
        from_attributes = True
