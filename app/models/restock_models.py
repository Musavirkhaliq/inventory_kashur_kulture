from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Restock(Base):
    __tablename__ = "restocks"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    restock_date = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
    )

    # Define the relationship with Product
    product = relationship("Product", back_populates="restocks")

# Import Product at the bottom to avoid circular imports
from .products_models import Product