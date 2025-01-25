# crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# Product CRUD
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
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if db_product:
        for var, value in vars(product).items():
            setattr(db_product, var, value)
        db_product.updated_at = datetime.utcnow()
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

# Sale CRUD
def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_amount=sale.total_amount,
        sale_date=datetime.utcnow()
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()

# Invoice CRUD
def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_invoice = models.Invoice(
        sale_id=invoice.sale_id,
        customer_name=invoice.customer_name,
        invoice_date=datetime.utcnow()
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Invoice).offset(skip).limit(limit).all()

# crud.py
from sqlalchemy import func

def get_sales_report(db: Session):
    return db.query(
        func.date(models.Sale.sale_date).label("sale_date"),
        func.sum(models.Sale.quantity).label("total_sales"),
        func.sum(models.Sale.total_amount).label("total_revenue")
    ).group_by(func.date(models.Sale.sale_date)).all()