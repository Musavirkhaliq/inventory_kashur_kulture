# app/models/cart_models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # If user auth exists
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    size = Column(String, nullable=True)
    
    product = relationship("Product", back_populates="cart_items")