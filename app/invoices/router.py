from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from ..models import invoice_models, sale_models,customer_models

from app.invoices.schemas import Invoice, InvoiceCreate
from app.invoices.services import get_all_invoices, create_invoice as create_invoice_service
from app.utils.utils import render_template

router = APIRouter(prefix="/invoices", tags=["invoices"])

# Route to display all invoices (HTML response)
@router.get("/", response_class=HTMLResponse)
def read_invoices(request: Request, db: Session = Depends(get_db)):
    invoices = get_all_invoices(db)
    return render_template("invoices.html", request, {"invoices": invoices})

# Route to create a new invoice (JSON response)
@router.post("/", response_model=Invoice)  
def create_invoice_route(invoice: InvoiceCreate, db: Session = Depends(get_db)): 
    try:
        return create_invoice_service(db, invoice)  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Route to generate an invoice (HTML response)
@router.get("/{invoice_id}", response_class=HTMLResponse)
def generate_invoice(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    invoice = (
        db.query(invoice_models.Invoice)
        .options(
            joinedload(invoice_models.Invoice.sale)  
            .joinedload(sale_models.Sale.items)  
            .joinedload(sale_models.SaleItem.product),  
            joinedload(invoice_models.Invoice.sale)  
            .joinedload(sale_models.Sale.customer)  
        )
        .filter(invoice_models.Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return render_template("invoice_template.html", request, {"invoice": invoice})


@router.get("/customers/balances", response_class=HTMLResponse)
def customer_balances(request: Request, db: Session = Depends(get_db)):
    customers = db.query(customer_models.Customer).all()
    return render_template("customer_balances.html", request, {"customers": customers})