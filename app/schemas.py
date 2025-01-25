# 4. **`schemas.py`**:
#    - **Purpose**: Defines Pydantic schemas for request/response validation.
#    - **Key Schemas**:
#      - `ProductCreate`: Schema for creating a product.
#      - `Product`: Schema for returning a product.
#      - Similar schemas for `sales`, `restocks`, and `invoices`.

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

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int

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