from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import JSONResponse
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.cart.services import (
    add_to_cart,
    get_cart_items,
    update_cart_item,
    remove_from_cart,
    CartUpdate
)
router = APIRouter(prefix="/cart", tags=["cart"])
from app.utils.utils import render_frontend_template


# View cart
@router.get("/", response_class=HTMLResponse)
def view_cart(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = None  
    cart_items = get_cart_items(db, user_id)
    
    subtotal = 0
    discount = 0
    for item in cart_items:
        subtotal += item.product.price * item.quantity
        discount += (item.product.original_price - item.product.price) * item.quantity
    
    delivery_charges = 50 if subtotal < 500 else 0  
    total = subtotal + delivery_charges
    return render_frontend_template(
        "product_cart.html",
        request,
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "discount": discount,
            "delivery_charges": delivery_charges,
            "total": total
        }
    )

# Add to cart
@router.post("/add/{product_id}", response_class=JSONResponse)
def add_to_cart_route(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[int] = Depends(get_current_user)
):
    user_id = current_user.id if current_user else None
    cart_item = add_to_cart(db, product_id, user_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found")
    return JSONResponse(content={"message": "Added to cart", "cart_id": cart_item.id})
# Update cart quantity
@router.post("/update/{cart_id}", response_class=HTMLResponse)
def update_cart_quantity_route(
    cart_id: int,
    cart_update: CartUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[int] = Depends(get_current_user)
):
    user_id = current_user.id if current_user else None
    updated_item = update_cart_item(db, cart_id, cart_update, user_id)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"success": True}

# Remove from cart
@router.get("/remove/{cart_id}", response_class=HTMLResponse)
def remove_from_cart_route(
    cart_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[int] = Depends(get_current_user)
):
    user_id = current_user.id if current_user else None
    removed_item = remove_from_cart(db, cart_id, user_id)
    if not removed_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return view_cart(request, db)  