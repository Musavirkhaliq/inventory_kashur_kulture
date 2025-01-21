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
