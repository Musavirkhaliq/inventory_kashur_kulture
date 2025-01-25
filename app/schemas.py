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



# ./app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Add Customer schemas
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    balance: Optional[float] = 0.0

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime  # Ensure created_at is included
    last_reminder: Optional[datetime] = None  # Ensure last_reminder is included

    class Config:
        from_attributes = True
# Update Sale schemas
class SaleBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: int
    amount_paid: float

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    total_amount: float
    sale_date: datetime

    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    sale_id: int
    customer_name: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    invoice_date: datetime

    class Config:
        from_attributes = True


# In app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# class CustomerBase(BaseModel):
#     name: str
#     email: str
#     phone: Optional[str] = None
#     balance: Optional[float] = 0.0

# class CustomerCreate(CustomerBase):
#     pass

# class Customer(CustomerBase):
#     id: int
#     created_at: datetime
#     last_reminder: Optional[datetime] = None

#     class Config:
#         from_attributes = True

