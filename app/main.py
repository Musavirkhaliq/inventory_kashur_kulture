from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import crud, schemas, models, database

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root Endpoint
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Product Endpoints
@app.get("/products", response_class=HTMLResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

# Sale Endpoints
@app.get("/sales", response_class=HTMLResponse)
def read_sales(request: Request, db: Session = Depends(get_db)):
    sales = crud.get_all_sales(db)
    return templates.TemplateResponse("sales.html", {"request": request, "sales": sales})

@app.post("/sales/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, sale)

# Restock Endpoints
@app.get("/restocks", response_class=HTMLResponse)
def read_restocks(request: Request, db: Session = Depends(get_db)):
    restocks = crud.get_all_restocks(db)
    return templates.TemplateResponse("restocks.html", {"request": request, "restocks": restocks})

@app.post("/restocks/", response_model=schemas.Restock)
def create_restock(restock: schemas.RestockCreate, db: Session = Depends(get_db)):
    return crud.create_restock(db, restock)

# Invoice Endpoints
@app.get("/invoices", response_class=HTMLResponse)
def read_invoices(request: Request, db: Session = Depends(get_db)):
    invoices = crud.get_all_invoices(db)
    return templates.TemplateResponse("invoices.html", {"request": request, "invoices": invoices})

@app.post("/invoices/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    return crud.create_invoice(db, invoice)


@app.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("edit_product.html", {"request": request, "product": product})

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# main.py
@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not crud.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# main.py
@app.get("/sales-report", response_class=HTMLResponse)
def read_sales_report(request: Request, db: Session = Depends(get_db)):
    sales_report = crud.get_sales_report(db)
    return templates.TemplateResponse("sales_report.html", {"request": request, "sales_report": sales_report})

# main.py
@app.get("/products/search", response_class=HTMLResponse)
def search_products(request: Request, query: str, db: Session = Depends(get_db)):
    products = crud.search_products(db, query)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})




# ./app/main.py
# Add these new endpoints

# Customer Endpoints
@app.get("/customers", response_class=HTMLResponse)
def read_customers(request: Request, db: Session = Depends(get_db)):
    customers = crud.get_all_customers(db)
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers})

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@app.post("/customers/{customer_id}/send-reminder")
def send_reminder(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.balance <= 0:
        raise HTTPException(status_code=400, detail="No outstanding balance")
    
    # Here you would implement actual reminder sending logic
    print(f"Reminder sent to {customer.name} (Balance: {customer.balance})")
    crud.record_reminder(db, customer_id)
    return {"message": "Reminder sent successfully"}


@app.post("/invoices/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    return crud.create_invoice(db, invoice)


# In app/main.py
@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_all_customers(db)
    return customers

@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id, customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return crud.delete_customer(db, customer_id)