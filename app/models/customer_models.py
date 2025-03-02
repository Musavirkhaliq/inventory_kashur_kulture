from sqlalchemy import CheckConstraint, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String)
    address = Column(String)
    balance_owe = Column(Float, default=0.0, nullable=False)

    __table_args__ = (
        CheckConstraint('balance_owe >= 0', name='check_positive_balance'),
    )

    sales = relationship("Sale", back_populates="customer")
    payments = relationship("Payment", back_populates="customer", lazy="joined")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount = Column(Float)
    method = Column(String)
    reference = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="payments")
# Import these here to avoid circular imports in the models
from ..models.sale_models import Sale
