from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InvoiceBase(BaseModel):
    sale_id: int
    invoice_date: datetime = datetime.now()
    due_date: Optional[datetime] = None
    paid: bool = False
    payment_date: Optional[datetime] = None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    
    class Config:
        orm_mode = True