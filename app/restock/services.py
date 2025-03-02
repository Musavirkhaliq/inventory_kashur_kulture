from sqlalchemy.orm import Session
from ..models.restock_models import Restock
from .schemas import RestockCreate

def get_all_restocks(db: Session):
    return db.query(Restock).all()

def create_restock(db: Session, restock: RestockCreate):
    # Calculate total cost
    total_cost = restock.quantity * restock.cost_per_unit
    
    # Create restock record
    db_restock = Restock(
        product_id=restock.product_id,
        quantity=restock.quantity,
        cost_per_unit=restock.cost_per_unit,
        total_cost=total_cost,
        restock_date=restock.restock_date
    )
    db.add(db_restock)
    
    # Update product inventory
    product = get_product_by_id(db, restock.product_id)
    if not product:
        db.rollback()
        raise ValueError(f"Product with ID {restock.product_id} not found")
    
    product.quantity += restock.quantity
    
    db.commit()
    db.refresh(db_restock)
    return db_restock