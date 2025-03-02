from sqlalchemy.orm import Session
from ..models.sale_models import Sale, SaleItem
from .schemas import SaleCreate, SaleItemCreate


def get_all_sales(db: Session):
    return db.query(Sale).all()

def create_sale(db: Session, sale: SaleCreate):
    # Create sale record
    db_sale = Sale(
        customer_id=sale.customer_id,
        sale_date=sale.sale_date,
        total_amount=sale.total_amount
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    # Create sale items and update inventory
    for item in sale.items:
        product = get_product_by_id(db, item.product_id)
        if not product:
            db.rollback()
            raise ValueError(f"Product with ID {item.product_id} not found")
        
        if product.quantity < item.quantity:
            db.rollback()
            raise ValueError(f"Insufficient stock for product {product.name}")
        
        # Create sale item
        db_sale_item = SaleItem(
            sale_id=db_sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_sale_item)
        
        # Update product inventory
        product.quantity -= item.quantity
    
    db.commit()
    db.refresh(db_sale)
    return db_sale