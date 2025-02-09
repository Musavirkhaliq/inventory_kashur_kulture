# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_positive_price'),
        CheckConstraint('quantity >= 0', name='check_positive_quantity'),
    )

    sale_items = relationship("SaleItem", back_populates="product")
    restocks = relationship("Restock", back_populates="product")

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


class SaleItem(Base):
    __tablename__ = 'sale_items'
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
        CheckConstraint('price >= 0', name='check_positive_price'),
    )

    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")

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

class Restock(Base):
    __tablename__ = "restocks"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    restock_date = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
    )

    product = relationship("Product", back_populates="restocks")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False, unique=True)
    invoice_date = Column(DateTime, default=func.now(), nullable=False)

    sale = relationship("Sale", back_populates="invoice")

from datetime import datetime
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
