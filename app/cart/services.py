from typing import Optional
from sqlalchemy.orm import Session
from app.models.products_models import Product
from app.models.cart_model import Cart
from app.products.schemas import ProductCreate, ProductUpdate, CartItem, CartUpdate
from app.products.services import get_product_by_id

# Existing services (get_all_products, get_product_by_id, etc.) unchanged...

def get_cart_items(db: Session, user_id: Optional[int] = None):
    """Fetch cart items for a user (or all if no user_id for simplicity here)."""
    query = db.query(Cart)
    if user_id:
        query = query.filter(Cart.user_id == user_id)
    return query.all()

def add_to_cart(db: Session, product_id: int, user_id: Optional[int] = None, quantity: int = 1, size: str = "M"):
    """Add or update item in cart."""
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    
    # Check if item exists in cart
    cart_item = db.query(Cart).filter(Cart.product_id == product_id, Cart.user_id == user_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(product_id=product_id, user_id=user_id, quantity=quantity, size=size)
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item

def update_cart_item(db: Session, cart_id: int, cart_update: CartUpdate, user_id: Optional[int] = None):
    """Update quantity or size of a cart item."""
    cart_item = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id).first()
    if not cart_item:
        return None
    
    if cart_update.quantity is not None:
        cart_item.quantity = cart_update.quantity
        if cart_item.quantity <= 0:
            db.delete(cart_item)
    if cart_update.size is not None:
        cart_item.size = cart_update.size
    
    db.commit()
    db.refresh(cart_item)
    return cart_item

def remove_from_cart(db: Session, cart_id: int, user_id: Optional[int] = None):
    """Remove item from cart."""
    cart_item = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id).first()
    if not cart_item:
        return None
    db.delete(cart_item)
    db.commit()
    return cart_item