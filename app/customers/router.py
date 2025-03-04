from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from ..models import customer_models
from app.customers.schemas import CustomerCreate, Customer, CustomerResponse
from app.customers.services import get_all_customers, get_customer_by_id, create_customer_service
from app.utils.utils import render_template

router = APIRouter(prefix="/customers", tags=["customers"])

# Route to display all customers (HTML response)
@router.get("/", response_class=HTMLResponse)
def read_customers(request: Request, db: Session = Depends(get_db)):
    customers = get_all_customers(db)
    return render_template("customers.html", request, {"customers": customers})

# Route to create a new customer (JSON response)
@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer_service(db, customer)

# Route to get a specific customer by ID (JSON response)
@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer_by_id(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Route to view transactions for a specific customer (HTML response)
@router.get("/{customer_id}/transactions", response_class=HTMLResponse)
def view_customer_transactions(request: Request, customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    transactions = db.query(customer_models.Sale).filter(customer_models.Sale.customer_id == customer_id).all()
    return render_template("customer_transactions.html", request, {"customer": customer, "transactions": transactions})

# Route to display customer balances (HTML response)
# @router.get("/customers/balances", response_class=HTMLResponse)
# def customer_balances(request: Request, db: Session = Depends(get_db)):
#     customers = db.query(customer_models.Customer).all()
#     return render_template("customer_balances.html", request, {"customers": customers})