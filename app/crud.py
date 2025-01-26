from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import List, Optional

# Utility functions
def get_product_by_id(db: Session, product_id: int) -> Optional[models.Product]:
    """Fetch a product by its ID."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_customer_by_id(db: Session, customer_id: int) -> Optional[models.Customer]:
    """Fetch a customer by their ID."""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

# Product CRUD
def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """Create a new product."""
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Get a product by its ID."""
    return get_product_by_id(db, product_id)

def get_all_products(db: Session) -> List[models.Product]:
    """Get all products."""
    return db.query(models.Product).all()

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate) -> Optional[models.Product]:
    """Update an existing product."""
    db_product = get_product_by_id(db, product_id)
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Delete a product by its ID."""
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# Customer CRUD
def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    """Create a new customer."""
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    """Get a customer by their ID."""
    return get_customer_by_id(db, customer_id)

def get_all_customers(db: Session) -> List[models.Customer]:
    """Get all customers."""
    return db.query(models.Customer).all()

# Sale CRUD
def create_sale(db: Session, sale: schemas.SaleCreate):
    try:
        # Fetch the product
        product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
        if not product:
            raise ValueError("Product not found")

        # Check if enough stock is available
        if product.quantity < sale.quantity:
            raise ValueError("Not enough stock available")

        # Fetch the customer
        customer = db.query(models.Customer).filter(models.Customer.id == sale.customer_id).first()
        if not customer:
            raise ValueError("Customer not found")

        # Calculate profit
        cost_price = product.price * sale.quantity
        profit = sale.selling_price - cost_price

        # Calculate balance
        balance = sale.selling_price - sale.amount_received

        # Update product quantity
        product.quantity -= sale.quantity

        # Update customer balance and transactions
        customer.balance_owe += balance  # Add remaining balance to customer's total balance
        if not customer.previous_transactions:
            customer.previous_transactions = []
        customer.previous_transactions.append({
            "sale_id": sale.product_id,
            "amount": sale.selling_price,
            "amount_received": sale.amount_received,
            "balance": balance,
            "date": datetime.now().isoformat(),
        })

        # Create the sale
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

    except Exception as e:
        db.rollback()  # Rollback the transaction on error
        raise e
    
    
def get_all_sales(db: Session) -> List[models.Sale]:
    """Get all sales."""
    return db.query(models.Sale).all()

# Restock CRUD
def create_restock(db: Session, restock: schemas.RestockCreate) -> models.Restock:
    """Create a new restock."""
    product = get_product_by_id(db, restock.product_id)
    if not product:
        raise ValueError("Product not found")
    
    product.quantity += restock.quantity

    db_restock = models.Restock(**restock.dict())
    db.add(db_restock)
    db.commit()
    db.refresh(db_restock)
    return db_restock

def get_all_restocks(db: Session) -> List[models.Restock]:
    """Get all restocks."""
    return db.query(models.Restock).all()

# Invoice CRUD
def create_invoice(db: Session, invoice: schemas.InvoiceCreate) -> models.Invoice:
    """Create a new invoice."""
    sale = db.query(models.Sale).filter(models.Sale.id == invoice.sale_id).first()
    if not sale:
        raise ValueError("Sale not found")
    
    db_invoice = models.Invoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_all_invoices(db: Session) -> List[models.Invoice]:
    """Get all invoices."""
    return db.query(models.Invoice).all()
