from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from ..models import sale_models
from app.sales.schemas import Sale, SaleCreate
from app.sales.services import get_all_sales, create_sale as create_sale_service
from app.products.services import get_all_products
from app.customers.services import get_all_customers
from app.utils.utils import render_template
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/sales", tags=["sales"])

# Route to display all sales (HTML response)
@router.get("/", response_class=HTMLResponse)
def read_sales(request: Request, db: Session = Depends(get_db)):
    products = get_all_products(db)
    customers = get_all_customers(db)
    sales = get_all_sales(db)
    return render_template("sales.html", request, {
        "products": products,
        "customers": customers,
        "sales": sales,
    })

# Route to create a new sale (JSON response)
@router.post("/", response_model=Sale)      
def create_sale_route(sale: SaleCreate, db: Session = Depends(get_db)):  
    try:
        return create_sale_service(db, sale)  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Route to get sale details (JSON response)
@router.get("/{sale_id}/details")
def get_sale_details(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(sale_models.Sale).filter(sale_models.Sale.id == sale_id).first()
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

# Route to generate sales report (HTML response)
@router.get("/report", response_class=HTMLResponse)
def sales_report(request: Request, db: Session = Depends(get_db)):
    # Fetch daily, weekly, and monthly sales data from the database
    daily_sales_records = db.query(sale_models.Sale).filter(sale_models.Sale.sale_date >= datetime.today().date()).all()
    weekly_sales_records = db.query(sale_models.Sale).filter(sale_models.Sale.sale_date >= datetime.today().date() - timedelta(days=7)).all()
    monthly_sales_records = db.query(sale_models.Sale).filter(sale_models.Sale.sale_date >= datetime.today().date() - timedelta(days=30)).all()

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

    return render_template("sales_report.html", request, {
        "daily_sales": daily_sales_records,
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