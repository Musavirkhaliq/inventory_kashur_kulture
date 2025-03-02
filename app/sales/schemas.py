from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class SaleItemCreate(SaleItemBase):
    pass

class SaleItem(SaleItemBase):
    id: int
    sale_id: int
    
    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    customer_id: int
    sale_date: datetime = datetime.now()
    total_amount: float

class SaleCreate(SaleBase):
    items: List[SaleItemCreate]

class Sale(SaleBase):
    id: int
    items: List[SaleItem] = []
    
    class Config:
        orm_mode = True