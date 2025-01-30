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



def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()  # Ensure changes are committed to the database
        return product  # Return the deleted product or details
    return None

# Customer CRUD
def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_all_customers(db: Session) -> List[models.Customer]:
    return db.query(models.Customer).all()


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



from sqlalchemy.exc import SQLAlchemyError

def create_sale(db: Session, sale: schemas.SaleCreate):
    # Calculate total amount and validate products
    total_amount = 0
    sale_items = []
    
    # Verify and process each item
    for item in sale.items:
        product = get_product_by_id(db, item.product_id)
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if product.quantity < item.quantity:
            raise ValueError(f"Insufficient stock for product {product.name}")
        
        subtotal = item.price * item.quantity
        total_amount += subtotal
        
        # Prepare sale item
        sale_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price
        })
        
        # Update product quantity
        product.quantity -= item.quantity

    # Calculate balance
    balance = total_amount - sale.amount_received

    # Create sale record
    db_sale = models.Sale(
        customer_id=sale.customer_id,
        total_amount=total_amount,
        amount_received=sale.amount_received,
        balance=balance,
        status="completed" if balance <= 0 else "pending"
    )
    
    try:
        db.add(db_sale)
        db.flush()  # Get the sale ID without committing

        # Create sale items
        for item_data in sale_items:
            sale_item = models.SaleItem(
                sale_id=db_sale.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price=item_data["price"]
            )
            db.add(sale_item)

        # Update the customer's balance_owe
        customer = db.query(models.Customer).filter_by(id=sale.customer_id).first()
        if customer:
            customer.balance_owe += balance

        db.commit()  # Commit all changes to the database
        db.refresh(db_sale)  # Refresh sale to get the updated data
        
        # Generate invoice automatically if paid in full
        if db_sale.status == "completed":
            create_invoice(db, schemas.InvoiceCreate(sale_id=db_sale.id))

        return db_sale

    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of any error
        raise Exception(f"An error occurred while creating the sale: {str(e)}")

def update_sale_payment(db: Session, sale_id: int, amount: float):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise ValueError("Sale not found")
    
    sale.amount_received += amount
    sale.balance = sale.total_amount - sale.amount_received
    
    if sale.balance <= 0:
        sale.status = "completed"
        # Generate invoice if not already generated
        if not sale.invoice:
            create_invoice(db, schemas.InvoiceCreate(sale_id=sale.id))
    
    db.commit()
    db.refresh(sale)
    return sale


from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate  # Import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)