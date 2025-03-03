from sqlalchemy.orm import Session
from ..models.invoice_models import Invoice
from .schemas import InvoiceCreate

def get_all_invoices(db: Session):
    return db.query(Invoice).all()

def create_invoice(db: Session, invoice: InvoiceCreate):
    # Check if invoice for this sale already exists
    existing_invoice = db.query(Invoice).filter(Invoice.sale_id == invoice.sale_id).first()
    if existing_invoice:
        raise ValueError(f"Invoice for sale ID {invoice.sale_id} already exists")
    
    # Create invoice record
    db_invoice = Invoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice