from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session,joinedload
from . import crud, schemas, models, database
from datetime import datetime, timedelta
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

# Helper function for rendering templates
def render_template(template_name: str, request: Request, context: dict = {}):
    context["request"] = request
    return templates.TemplateResponse(template_name, context)

# Root Endpoint
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return render_template("index.html", request)

# Product Endpoints
@app.get("/products", response_class=HTMLResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    return render_template("products.html", request, {"products": products})

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return render_template("edit_product.html", request, {"product": product})

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Customer Endpoints
@app.get("/customers", response_class=HTMLResponse)
def read_customers(request: Request, db: Session = Depends(get_db)):
    customers = crud.get_all_customers(db)
    return render_template("customers.html", request, {"customers": customers})

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

# Sale Endpoints
@app.get("/sales", response_class=HTMLResponse)
def read_sales(request: Request, db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    customers = crud.get_all_customers(db)
    sales = crud.get_all_sales(db)
    return render_template("sales.html", request, {
        "products": products,
        "customers": customers,
        "sales": sales,
    })

@app.post("/sales/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_sale(db, sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Restock Endpoints
@app.get("/restocks", response_class=HTMLResponse)
def read_restocks(request: Request, db: Session = Depends(get_db)):
    restocks = crud.get_all_restocks(db)
    products = crud.get_all_products(db)  # Fetch all products
    return templates.TemplateResponse(
        "restocks.html",
        {"request": request, "restocks": restocks, "products": products},
    )


@app.post("/restocks/", response_model=schemas.Restock)
def create_restock(restock: schemas.RestockCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_restock(db, restock)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Invoice Endpoints
@app.get("/invoices", response_class=HTMLResponse)
def read_invoices(request: Request, db: Session = Depends(get_db)):
    invoices = crud.get_all_invoices(db)
    return render_template("invoices.html", request, {"invoices": invoices})

@app.post("/invoices/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_invoice(db, invoice)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/invoices/{invoice_id}", response_class=HTMLResponse)
def generate_invoice(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    invoice = (
        db.query(models.Invoice)
        .options(
            joinedload(models.Invoice.sale)
            .joinedload(models.Sale.items)  # Load sale items
            .joinedload(models.SaleItem.product),  # Load products through SaleItem
            joinedload(models.Invoice.sale)
            .joinedload(models.Sale.customer)  # Load customer details
        )
        .filter(models.Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return templates.TemplateResponse(
        "invoice_template.html",
        {"request": request, "invoice": invoice}
    )


@app.get("/customers/{customer_id}/transactions", response_class=HTMLResponse)
def view_customer_transactions(request: Request, customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    transactions = db.query(models.Sale).filter(models.Sale.customer_id == customer_id).all()
    return render_template("customer_transactions.html", request, {"customer": customer, "transactions": transactions})


# @app.get("/sales/report", response_class=HTMLResponse)
# def sales_report(request: Request, db: Session = Depends(get_db)):
#     daily_sales = db.query(models.Sale).filter(models.Sale.sale_date >= datetime.today().date()).all()
#     weekly_sales = db.query(models.Sale).filter(models.Sale.sale_date >= datetime.today().date() - timedelta(days=7)).all()
#     monthly_sales = db.query(models.Sale).filter(models.Sale.sale_date >= datetime.today().date() - timedelta(days=30)).all()

#     daily_total = sum(sale.total_amount  for sale in daily_sales)
#     weekly_total = sum(sale.total_amount  for sale in weekly_sales)
#     monthly_total = sum(sale.total_amount  for sale in monthly_sales)

#     return render_template("sales_report.html", request, {
#         "daily_sales": daily_sales,
#         "weekly_sales": weekly_sales,
#         "monthly_sales": monthly_sales,
#         "daily_total": daily_total,
#         "weekly_total": weekly_total,
#         "monthly_total": monthly_total,
#     })

@app.get("/customers/balances", response_class=HTMLResponse)
def customer_balances(request: Request, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return render_template("customer_balances.html", request, {"customers": customers})


@app.get("/inventory/value", response_class=HTMLResponse)
def inventory_value(request: Request, db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    total_value = sum(product.price * product.quantity for product in products)
    return render_template("inventory_value.html", request, {"total_value": total_value})

@app.get("/sales/{sale_id}/details")
def get_sale_details(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {
        "id": sale.id,
        "customer_name": sale.customer.name,
        "total_amount": sale.total_amount,
        "items": [{
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": item.price,
        } for item in sale.items]
    }


@app.get("/sales/report", response_class=HTMLResponse)
def sales_report(request: Request, db: Session = Depends(get_db)):
    # Fetch daily, weekly, and monthly sales data from the database
    daily_sales_records = db.query(models.Sale).filter(models.Sale.sale_date >= datetime.today().date()).all()
    weekly_sales_records = db.query(models.Sale).filter(models.Sale.sale_date >= datetime.today().date() - timedelta(days=7)).all()
    monthly_sales_records = db.query(models.Sale).filter(models.Sale.sale_date >= datetime.today().date() - timedelta(days=30)).all()

    # Calculate total sales
    daily_sales_total = sum(sale.total_amount for sale in daily_sales_records)
    weekly_sales_total = sum(sale.total_amount for sale in weekly_sales_records)
    monthly_sales_total = sum(sale.total_amount for sale in monthly_sales_records)

    # Prepare chart data
    daily_sales_labels = [sale.sale_date.strftime("%Y-%m-%d") for sale in daily_sales_records]
    daily_sales_data = [sale.total_amount for sale in daily_sales_records]

    weekly_sales_labels = [sale.sale_date.strftime("%Y-%m-%d") for sale in weekly_sales_records]
    weekly_sales_data = [sale.total_amount for sale in weekly_sales_records]

    monthly_sales_labels = [sale.sale_date.strftime("%Y-%m") for sale in monthly_sales_records]
    monthly_sales_data = [sale.total_amount for sale in monthly_sales_records]

    return templates.TemplateResponse("sales_report.html", {
        "request": request,
        "daily_sales": daily_sales_records,  # Keep the original records if needed
        "daily_total": daily_sales_total,
        "daily_sales_labels": daily_sales_labels,
        "daily_sales_data": daily_sales_data,
        "weekly_sales": weekly_sales_records,
        "weekly_total": weekly_sales_total,
        "weekly_sales_labels": weekly_sales_labels,
        "weekly_sales_data": weekly_sales_data,
        "monthly_sales": monthly_sales_records,
        "monthly_total": monthly_sales_total,
        "monthly_sales_labels": monthly_sales_labels,
        "monthly_sales_data": monthly_sales_data,
    })