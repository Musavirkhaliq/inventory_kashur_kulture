from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.products.schemas import Product, ProductCreate, ProductUpdate  
from app.products.services import (
    get_all_products, 
    get_product_by_id, 
    create_product as create_product_service, 
    update_product as update_product_service, 
    delete_product as delete_product_service, 
)
from app.utils.utils import render_template 

router = APIRouter(prefix="/products", tags=["products"])

# Route to display all products (HTML response)
@router.get("/", response_class=HTMLResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = get_all_products(db)
    return render_template("products.html", request, {"products": products})

# Route to create a new product (JSON response)
@router.post("/", response_model=Product)  
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):  
    return create_product_service(db, product)  

# Route to edit a product (HTML response)
@router.get("/{product_id}/edit", response_class=HTMLResponse)
def edit_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return render_template("edit_product.html", request, {"product": product})

# Route to update a product (JSON response)
@router.put("/{product_id}", response_model=Product)  
def update_product_route(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):  
    db_product = update_product_service(db, product_id, product)  
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Route to delete a product (JSON response)
@router.delete("/{product_id}", response_model=Product) 
def delete_product_route(product_id: int, db: Session = Depends(get_db)):  
    db_product = delete_product_service(db, product_id)  
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Route to calculate and display inventory value (HTML response)
@router.get("/inventory/value", response_class=HTMLResponse)
def inventory_value(request: Request, db: Session = Depends(get_db)):
    products = get_all_products(db)
    total_value = sum(product.price * product.quantity for product in products)
    return render_template("inventory_value.html", request, {"total_value": total_value})