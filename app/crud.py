from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# Product CRUD
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(models.Product).all()

# Customer CRUD
def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_all_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

# Sale CRUD
def create_sale(db: Session, sale: schemas.SaleCreate):
    # Fetch the product to get its cost price
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    if not product:
        raise ValueError("Product not found")

    # Fetch the customer to update their balance and transactions
    customer = db.query(models.Customer).filter(models.Customer.id == sale.customer_id).first()
    if not customer:
        raise ValueError("Customer not found")

    # Calculate profit
    cost_price = product.price * sale.quantity
    profit = sale.selling_price - cost_price

    # Update customer balance and transactions
    customer.balance_owe += sale.selling_price
    customer.previous_transactions.append({
        "sale_id": sale.id,
        "amount": sale.selling_price,
        "date": datetime.now().isoformat(),
    })

    # Create the sale with the calculated profit
    db_sale = models.Sale(
        product_id=sale.product_id,
        customer_id=sale.customer_id,
        quantity=sale.quantity,
        selling_price=sale.selling_price,
        profit=profit,
    )
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