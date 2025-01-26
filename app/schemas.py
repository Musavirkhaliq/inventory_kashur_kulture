from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    balance_owe: Optional[float] = 0.0
    previous_transactions: Optional[List[dict]] = []

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: int
    selling_price: float  # Selling price entered by the user
    profit: float  # Calculated profit

class SaleCreate(BaseModel):
    product_id: int
    customer_id: int
    quantity: int
    selling_price: float

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

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None