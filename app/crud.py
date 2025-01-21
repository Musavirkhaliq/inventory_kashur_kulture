# crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(models.Product.sku == sku).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        sku=product.sku,
        quantity=product.quantity,
        price=product.price,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
    except Exception as e:
        db.rollback()
        raise e
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if db_product:
        for var, value in vars(product).items():
            setattr(db_product, var, value)
        db_product.updated_at = datetime.utcnow()
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False