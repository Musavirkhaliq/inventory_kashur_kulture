from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.products_models import Product
from .schemas import ProductCreate, ProductUpdate

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    # Calculate discount percentage if original_price is provided
    product_dict = product.dict()
    if product_dict.get('original_price') and product_dict.get('price'):
        original = product_dict['original_price']
        sale = product_dict['price']
        if original > 0:
            discount = ((original - sale) / original) * 100
            product_dict['discount_percentage'] = round(discount, 2)
            product_dict['price'] = sale
        else:
            product_dict['discount_percentage'] = 0
            product_dict['price'] = sale
    
    db_product = Product(**product_dict)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    
    update_data = product.dict(exclude_unset=True)
    
    # Recalculate discount percentage if price or original_price is updated
    if 'price' in update_data or 'original_price' in update_data:
        original = update_data.get('original_price', db_product.original_price)
        sale = update_data.get('price', db_product.price)
        if original > 0:
            discount = ((original - sale) / original) * 100
            update_data['discount_percentage'] = round(discount, 2)
            update_data['price'] = sale
    
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    
    db.delete(db_product)
    db.commit()
    return db_product

def get_filter_counts(db: Session):
    """Get counts for different filter categories to display in filter sidebar"""
    
    # Gender counts
    gender_counts = db.query(Product.gender, func.count(Product.id)) \
                   .group_by(Product.gender) \
                   .all()
    gender_counts_dict = {gender: count for gender, count in gender_counts if gender}
    
    # Category counts
    category_counts = db.query(Product.category, func.count(Product.id)) \
                     .group_by(Product.category) \
                     .all()
    category_counts_dict = {category: count for category, count in category_counts if category}
    
    # Brand counts
    brand_counts = db.query(Product.brand, func.count(Product.id)) \
                  .group_by(Product.brand) \
                  .all()
    brand_counts_dict = {brand: count for brand, count in brand_counts}
    
    return {
        'gender_counts': gender_counts_dict,
        'category_counts': category_counts_dict,
        'brand_counts': brand_counts_dict
    }

# New service for similar products
def get_similar_products(db: Session, product: Product, limit: int = 4):
    """
    Fetch similar products based on category and/or brand, excluding the current product.
    """
    query = db.query(Product).filter(Product.id != product.id)
    
    # Prioritize same category and brand
    similar = query.filter(
        (Product.category == product.category) |
        (Product.brand == product.brand)
    ).limit(limit).all()
    
    # If not enough results, fill with random products
    if len(similar) < limit:
        additional = query.filter(
            Product.id.notin_([p.id for p in similar])
        ).limit(limit - len(similar)).all()
        similar.extend(additional)
    
    return similar[:limit]
