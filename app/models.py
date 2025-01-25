from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

# # Product model
# class Product(Base):
#     __tablename__ = "products"  # Table name
#     id = Column(Integer, primary_key=True, index=True)  # Primary key
#     name = Column(String, index=True)  # Product name
#     description = Column(String, nullable=True)  # Product description (optional)
#     price = Column(Float)  # Product price
#     quantity = Column(Integer)  # Product quantity

# # Sale model
# class Sale(Base):
#     __tablename__ = "sales"  # Table name
#     id = Column(Integer, primary_key=True, index=True)  # Primary key
#     product_id = Column(Integer, ForeignKey("products.id"))  # Foreign key to products
#     quantity = Column(Integer)  # Quantity sold
#     sale_date = Column(DateTime, default=func.now())  # Sale date (auto-generated)

# Restock model
class Restock(Base):
    __tablename__ = "restocks"  # Table name
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    product_id = Column(Integer, ForeignKey("products.id"))  # Foreign key to products
    quantity = Column(Integer)  # Quantity restocked
    restock_date = Column(DateTime, default=func.now())  # Restock date (auto-generated)

# Invoice model
class Invoice(Base):
    __tablename__ = "invoices"  # Table name
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    sale_id = Column(Integer, ForeignKey("sales.id"))  # Foreign key to sales
    invoice_date = Column(DateTime, default=func.now())  # Invoice date (auto-generated)




    # ./app/models.py
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

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())
    last_reminder = Column(DateTime, nullable=True)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    quantity = Column(Integer)
    total_amount = Column(Float)
    amount_paid = Column(Float)
    sale_date = Column(DateTime, default=func.now())

# Restock and Invoice models remain the same