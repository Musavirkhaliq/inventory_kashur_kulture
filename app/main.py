# 5. **`main.py`**:
#    - **Purpose**: Defines the FastAPI application and API routes.
#    - **Key Routes**:
#      - `/products/`: Handles product-related operations (e.g., create, read, update).
#      - `/sales/`: Handles sale-related operations.
#      - `/restocks/`: Handles restock-related operations.
#      - `/invoices/`: Handles invoice-related operations.

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