# 1. **`crud.py`**:
#    - **Purpose**: Contains functions to perform CRUD (Create, Read, Update, Delete) operations on the database.
#    - **Key Functions**:
#      - `create_product`: Adds a new product to the database.
#      - `get_product`: Retrieves a product by its ID.
#      - `get_all_products`: Retrieves all products from the database.
#      - `update_product`: Updates an existing product.
#      - Similar functions for `sales`, `restocks`, and `invoices`.


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