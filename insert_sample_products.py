from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import products_models  # Adjust the import based on your project structure

# Database setup
DATABASE_URL = "sqlite:///./inventory.db"  
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# Sample data for 30 products
sample_products = [
    {
        "name": "Men's Casual Shirt",
        "description": "Comfortable and stylish casual shirt for men, perfect for everyday wear.",
        "price": 29.99,
        "quantity": 100,
        "brand": "Brand A",
        "original_price": 39.99,
        "price": 29.99,
        "discount_percentage": 25.0,
        "image_url": "https://example.com/images/mens_casual_shirt.jpg",
        "is_bestseller": True,
        "category": "Clothing",
        "gender": "Male",
    },
    {
        "name": "Women's Summer Dress",
        "description": "Lightweight and elegant summer dress for women, ideal for sunny days.",
        "price": 49.99,
        "quantity": 80,
        "brand": "Brand B",
        "original_price": 59.99,
        "price": 49.99,
        "discount_percentage": 16.67,
        "image_url": "https://example.com/images/womens_summer_dress.jpg",
        "is_bestseller": True,
        "category": "Clothing",
        "gender": "Female",
    },
    {
        "name": "Wireless Bluetooth Earbuds",
        "description": "High-quality wireless earbuds with noise cancellation and long battery life.",
        "price": 79.99,
        "quantity": 120,
        "brand": "Brand C",
        "original_price": 99.99,
        "price": 79.99,
        "discount_percentage": 20.0,
        "image_url": "https://example.com/images/wireless_earbuds.jpg",
        "is_bestseller": True,
        "category": "Electronics",
        "gender": "Unisex",
    },
    {
        "name": "Leather Wallet",
        "description": "Premium leather wallet with multiple card slots and a sleek design.",
        "price": 19.99,
        "quantity": 150,
        "brand": "Brand D",
        "original_price": 29.99,
        "price": 19.99,
        "discount_percentage": 33.33,
        "image_url": "https://example.com/images/leather_wallet.jpg",
        "is_bestseller": False,
        "category": "Accessories",
        "gender": "Male",
    },
    {
        "name": "Women's Running Shoes",
        "description": "Lightweight and durable running shoes designed for women.",
        "price": 89.99,
        "quantity": 90,
        "brand": "Brand E",
        "original_price": 109.99,
        "price": 89.99,
        "discount_percentage": 18.18,
        "image_url": "https://example.com/images/womens_running_shoes.jpg",
        "is_bestseller": True,
        "category": "Footwear",
        "gender": "Female",
    },
    {
        "name": "Smartwatch Fitness Tracker",
        "description": "Track your fitness goals with this advanced smartwatch.",
        "price": 129.99,
        "quantity": 70,
        "brand": "Brand F",
        "original_price": 149.99,
        "price": 129.99,
        "discount_percentage": 13.33,
        "image_url": "https://example.com/images/smartwatch.jpg",
        "is_bestseller": True,
        "category": "Electronics",
        "gender": "Unisex",
    },
    {
        "name": "Men's Formal Suit",
        "description": "Elegant formal suit for men, perfect for business meetings and events.",
        "price": 199.99,
        "quantity": 50,
        "brand": "Brand A",
        "original_price": 249.99,
        "price": 199.99,
        "discount_percentage": 20.0,
        "image_url": "https://example.com/images/mens_formal_suit.jpg",
        "is_bestseller": False,
        "category": "Clothing",
        "gender": "Male",
    },
    {
        "name": "Women's Handbag",
        "description": "Stylish and spacious handbag for women, perfect for daily use.",
        "price": 59.99,
        "quantity": 110,
        "brand": "Brand B",
        "original_price": 79.99,
        "price": 59.99,
        "discount_percentage": 25.0,
        "image_url": "https://example.com/images/womens_handbag.jpg",
        "is_bestseller": True,
        "category": "Accessories",
        "gender": "Female",
    },
    {
        "name": "Gaming Keyboard",
        "description": "Mechanical gaming keyboard with RGB lighting and customizable keys.",
        "price": 89.99,
        "quantity": 60,
        "brand": "Brand C",
        "original_price": 109.99,
        "price": 89.99,
        "discount_percentage": 18.18,
        "image_url": "https://example.com/images/gaming_keyboard.jpg",
        "is_bestseller": False,
        "category": "Electronics",
        "gender": "Unisex",
    },
    {
        "name": "Men's Leather Jacket",
        "description": "Classic leather jacket for men, offering style and durability.",
        "price": 149.99,
        "quantity": 40,
        "brand": "Brand D",
        "original_price": 199.99,
        "price": 149.99,
        "discount_percentage": 25.0,
        "image_url": "https://example.com/images/mens_leather_jacket.jpg",
        "is_bestseller": True,
        "category": "Clothing",
        "gender": "Male",
    },
    # Add more products here...
]

# Insert sample data into the database
db = SessionLocal()
try:
    for product_data in sample_products:
        product = products_models.Product(**product_data)
        db.add(product)
    db.commit()
    print("30 sample products inserted successfully!")
except Exception as e:
    db.rollback()
    print(f"Error inserting products: {e}")
finally:
    db.close()