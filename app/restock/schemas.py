from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RestockBase(BaseModel):
    product_id: int
    quantity: int
    cost_per_unit: float
    restock_date: datetime = datetime.now()

class RestockCreate(RestockBase):
    pass

class Restock(RestockBase):
    id: int
    total_cost: float
    
    class Config:
        orm_mode = True