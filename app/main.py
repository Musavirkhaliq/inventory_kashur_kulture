# main.py
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Get the current directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount static files and templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/products")
async def products(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return templates.TemplateResponse("products.html", {
        "request": request,
        "products": products
    })

@app.post("/api/products")
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/api/products")
async def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.post("/api/sales")
async def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    # Check if product exists and has enough stock
    product = crud.get_product(db, sale.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Update product stock
    product.quantity -= sale.quantity
    db.commit()

    # Create sale
    return crud.create_sale(db, sale)

@app.post("/api/invoices")
async def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    return crud.create_invoice(db, invoice)

@app.get("/api/invoices")
async def read_invoices(db: Session = Depends(get_db)):
    return crud.get_invoices(db)


# main.py
@app.get("/invoices")
async def invoices(request: Request, db: Session = Depends(get_db)):
    invoices = crud.get_invoices(db)
    return templates.TemplateResponse("invoices.html", {
        "request": request,
        "invoices": invoices
    })


# main.py
@app.get("/sales-report")
async def sales_report(request: Request, db: Session = Depends(get_db)):
    sales_report = crud.get_sales_report(db)
    return templates.TemplateResponse("sales_report.html", {
        "request": request,
        "sales_report": sales_report
    })


# main.py
@app.post("/api/sales")
async def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    # Check if product exists and has enough stock
    product = crud.get_product(db, sale.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Calculate total amount
    total_amount = product.price * sale.quantity

    # Update product stock
    product.quantity -= sale.quantity
    db.commit()

    # Create sale
    db_sale = models.Sale(
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_amount=total_amount,
        sale_date=datetime.utcnow()
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    # Create invoice
    db_invoice = models.Invoice(
        sale_id=db_sale.id,
        customer_name=sale.customer_name,
        invoice_date=datetime.utcnow()
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    return db_sale