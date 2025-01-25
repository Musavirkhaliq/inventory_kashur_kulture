from sqlalchemy.orm import Session
from . import models, schemas

# Product CRUD
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    print(db_product.__dict__)  # Log the created product
    return db_product   

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(models.Product).all()

# Sale CRUD
def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_all_sales(db: Session):
    return db.query(models.Sale).all()

# Restock CRUD
def create_restock(db: Session, restock: schemas.RestockCreate):
    db_restock = models.Restock(**restock.dict())
    db.add(db_restock)
    db.commit()
    db.refresh(db_restock)
    print(db_restock.__dict__)  # Log the created restock
    return db_restock

def get_all_restocks(db: Session):
    return db.query(models.Restock).all()

# Invoice CRUD
def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_invoice = models.Invoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_all_invoices(db: Session):
    return db.query(models.Invoice).all()


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


# crud.py
def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


# crud.py
def create_sale(db: Session, sale: schemas.SaleCreate):
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    product.quantity -= sale.quantity  # Deduct stock
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


# crud.py
from sqlalchemy import func

def get_sales_report(db: Session):
    return db.query(
        func.date(models.Sale.sale_date).label("sale_date"),
        func.sum(models.Sale.quantity).label("total_sales"),
        func.sum(models.Sale.quantity * models.Product.price).label("total_revenue")
    ).join(models.Product).group_by(func.date(models.Sale.sale_date)).all()

# crud.py
def search_products(db: Session, query: str):
    return db.query(models.Product).filter(
        (models.Product.name.contains(query)) | (models.Product.description.contains(query))
    ).all()



# ./app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from datetime import datetime

# Customer CRUD operations
def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_all_customers(db: Session):
    return db.query(models.Customer).all()

def update_customer_balance(db: Session, customer_id: int, amount: float):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer:
        customer.balance += amount
        db.commit()
        db.refresh(customer)
    return customer

def record_reminder(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer:
        customer.last_reminder = datetime.now()
        db.commit()
        db.refresh(customer)
    return customer

def get_overdue_customers(db: Session):
    return db.query(models.Customer).filter(models.Customer.balance > 0).all()

# Update create_sale function
def create_sale(db: Session, sale: schemas.SaleCreate):
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    customer = db.query(models.Customer).filter(models.Customer.id == sale.customer_id).first()
    
    if not product or not customer:
        raise HTTPException(status_code=404, detail="Product or Customer not found")
    
    if product.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    total_amount = product.price * sale.quantity
    if sale.amount_paid > total_amount:
        raise HTTPException(status_code=400, detail="Amount paid exceeds total")
    
    product.quantity -= sale.quantity
    customer.balance += (total_amount - sale.amount_paid)
    
    db_sale = models.Sale(
        **sale.dict(),
        total_amount=total_amount
    )
    
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale