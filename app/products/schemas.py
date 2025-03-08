from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    brand: str = Field(..., description="Brand of the product")
    image_url: Optional[str] = None  # For product image
    category: Optional[str] = None   # For filtering (e.g., Dresses, Shirts)
    gender: Optional[str] = None     # For filtering (e.g., Women, Men)
    original_price: float = Field(..., description="Original price before discount")
    price: float = Field(..., description="Price after discount")
    discount_percentage: Optional[float] = Field(None, description="Discount percentage")
    is_bestseller: Optional[bool] = Field(False, description="Flag to mark bestselling products")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    original_price: Optional[float] = None
    price: Optional[float] = None
    discount_percentage: Optional[float] = None
    is_bestseller: Optional[bool] = None

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  # For Pydantic v2

class CartItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    size: Optional[str] = None

    class Config:
        orm_mode = True  # Pydantic V1; use from_attributes=True for V2

class CartUpdate(BaseModel):
    quantity: Optional[int] = None
    size: Optional[str] = None