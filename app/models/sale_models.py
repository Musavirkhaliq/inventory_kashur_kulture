from sqlalchemy import CheckConstraint, Column, Integer, Float, ForeignKey,String, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    amount_received = Column(Float, default=0.0, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    sale_date = Column(DateTime, default=func.now(), nullable=False)
    status = Column(String, default="pending", nullable=False)

    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='check_positive_total'),
        CheckConstraint('amount_received >= 0', name='check_positive_received'),
    )

    customer = relationship("Customer", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates="sale", uselist=False)

class SaleItem(Base):
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)
    
    # Relationships
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")

# Import these to avoid circular imports
from .customer_models import Customer
from .products_models import Product
from .invoice_models import Invoice
from .restock_models import Restock