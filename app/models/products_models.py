from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    quantity = Column(Integer, default=0)
    brand = Column(String, nullable=False)
    original_price = Column(Float, nullable=False)
    discount_percentage = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    is_bestseller = Column(Boolean, default=False)
    category = Column(String, nullable=True)
    gender = Column(String, nullable=True)

    cart_items = relationship("Cart", back_populates="product")
    restocks = relationship("Restock", back_populates="product")



