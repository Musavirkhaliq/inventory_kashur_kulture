# 3. **`models.py`**:
#    - **Purpose**: Defines the database models using SQLAlchemy.
#    - **Key Models**:
#      - `Product`: Represents a product in the inventory.
#      - `Sale`: Represents a sale transaction.
#      - `Restock`: Represents a restock transaction.
#      - `Invoice`: Represents an invoice for a sale.

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    quantity = Column(Integer)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    sale_date = Column(DateTime, default=func.now())

class Restock(Base):
    __tablename__ = "restocks"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    restock_date = Column(DateTime, default=func.now())

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    invoice_date = Column(DateTime, default=func.now())