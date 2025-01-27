from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import List, Optional

# Utility functions
def get_product_by_id(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_customer_by_id(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

# Product CRUD
def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session) -> List[models.Product]:
    return db.query(models.Product).all()



def delete_product(db: Session, product_id: int) -> Optional[models.Product]:
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# Customer CRUD
def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_all_customers(db: Session) -> List[models.Customer]:
    return db.query(models.Customer).all()

# Sale CRUD
def create_sale(db: Session, sale: schemas.SaleCreate):
    product = get_product_by_id(db, sale.product_id)
    if not product:
        raise ValueError("Product not found")
    if product.quantity < sale.quantity:
        raise ValueError("Not enough stock available")

    customer = get_customer_by_id(db, sale.customer_id)
    if not customer:
        raise ValueError("Customer not found")

    profit = (sale.selling_price*sale.quantity) - (product.price * sale.quantity)
    balance = (sale.selling_price*sale.quantity) - sale.amount_received

    product.quantity -= sale.quantity
    customer.balance_owe += balance

    db_sale = models.Sale(
        product_id=sale.product_id,
        customer_id=sale.customer_id,
        quantity=sale.quantity,
        selling_price=sale.selling_price,
        amount_received=sale.amount_received,
        balance=balance,
        profit=profit,
    )

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_all_sales(db: Session) -> List[models.Sale]:
    return db.query(models.Sale).all()

# Restock CRUD
def create_restock(db: Session, restock: schemas.RestockCreate):
    db_restock = models.Restock(**restock.dict())
    db.add(db_restock)
    db.commit()
    db.refresh(db_restock)

    # Update product quantity
    product = db.query(models.Product).filter(models.Product.id == restock.product_id).first()
    if product:
        product.quantity += restock.quantity  # Add restocked quantity
        db.commit()
        db.refresh(product)

    return db_restock

def get_all_restocks(db: Session) -> List[models.Restock]:
    return db.query(models.Restock).all()

# Invoice CRUD
def create_invoice(db: Session, invoice: schemas.InvoiceCreate) -> models.Invoice:
    sale = db.query(models.Sale).filter(models.Sale.id == invoice.sale_id).first()
    if not sale:
        raise ValueError("Sale not found")

    db_invoice = models.Invoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_all_invoices(db: Session) -> List[models.Invoice]:
    return db.query(models.Invoice).all()

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# def update_product(db: Session, product_id: int, product: schemas.ProductUpdate) -> Optional[models.Product]:
#     db_product = get_product_by_id(db, product_id)
#     if db_product:
#         for key, value in product.dict(exclude_unset=True).items():
#             setattr(db_product, key, value)
#         db.commit()
#         db.refresh(db_product)
#     return db_product

