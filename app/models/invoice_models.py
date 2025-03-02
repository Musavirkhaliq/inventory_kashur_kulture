from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False, unique=True)
    invoice_date = Column(DateTime, default=func.now(), nullable=False)
    sale = relationship("Sale", back_populates="invoice")

# Import these to avoid circular imports
from .sale_models import Sale