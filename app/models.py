from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

# class Product(Base):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String, nullable=True)
#     price = Column(Float)
#     quantity = Column(Integer)

#     sales = relationship("Sale", back_populates="product")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    address = Column(String)
    balance_owe = Column(Float, default=0.0)
    previous_transactions = Column(JSON, default=[])

    sales = relationship("Sale", back_populates="customer")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    quantity = Column(Integer)
    selling_price = Column(Float)
    amount_received = Column(Float)
    balance = Column(Float)
    profit = Column(Float)
    sale_date = Column(DateTime, default=func.now())

    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    invoice = relationship("Invoice", back_populates="sale", uselist=False)

class Restock(Base):
    __tablename__ = "restocks"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    restock_date = Column(DateTime, default=func.now())

    # Add relationship to Product
    product = relationship("Product", back_populates="restocks")
    

# Add back-populate to Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    quantity = Column(Integer)

    # Define relationships
    sales = relationship("Sale", back_populates="product")  # Relationship to Sale
    restocks = relationship("Restock", back_populates="product")  # Relationship to Restock
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    invoice_date = Column(DateTime, default=func.now())

    sale = relationship("Sale", back_populates="invoice")