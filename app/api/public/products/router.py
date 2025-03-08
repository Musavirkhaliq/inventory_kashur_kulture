from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.products.schemas import Product, ProductCreate, ProductUpdate
from app.products.services import (
    get_all_products,
    get_product_by_id,
    get_filter_counts,
    get_similar_products,  # New service to be added
)
from app.cart.services import (
    add_to_cart,
    get_cart_items,
    update_cart_item,
    remove_from_cart,
    CartUpdate
)
from app.utils.utils import render_frontend_template

router = APIRouter(prefix="/filter-products", tags=["filter-products"])

# Existing route for filtered product listing
@router.get("/", response_class=HTMLResponse)
def read_products(
    request: Request,
    gender: Optional[List[str]] = Query(None),
    category: Optional[List[str]] = Query(None),
    brand: Optional[List[str]] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("relevance"),
    db: Session = Depends(get_db)
):
    products = get_all_products(db)
    
    # Apply search filter
    if search and search.strip():
        search_term = search.lower()
        products = [p for p in products if 
                   search_term in p.name.lower() or 
                   (p.description and search_term in p.description.lower()) or
                   (p.category and search_term in p.category.lower())]
    
    # Apply filters
    if gender:
        products = [p for p in products if p.gender in gender]
    if category:
        products = [p for p in products if p.category in category]
    if brand:
        products = [p for p in products if p.brand in brand]
    if min_price is not None:
        products = [p for p in products if p.price >= min_price]
    if max_price is not None:
        products = [p for p in products if p.price <= max_price]
    
    # Apply sorting
    if sort_by == "price_low":
        products.sort(key=lambda p: p.price)
    elif sort_by == "price_high":
        products.sort(key=lambda p: p.price, reverse=True)
    elif sort_by == "discount":
        products.sort(key=lambda p: p.discount_percentage or 0, reverse=True)
    elif sort_by == "new":
        products.sort(key=lambda p: p.id, reverse=True)  # Proxy for newest
    
    # Get filter counts
    filter_counts = get_filter_counts(db)
    
    return render_frontend_template(
        "products.html",
        request,
        {
            "products": products,
            "gender_counts": filter_counts["gender_counts"],
            "category_counts": filter_counts["category_counts"],
            "brand_counts": filter_counts["brand_counts"],
            "selected_gender": gender,
            "selected_category": category,
            "selected_brand": brand,
            "min_price": min_price,
            "max_price": max_price,
            "search_query": search,
            "sort_by": sort_by
        }
    )

# New route for product detail page
@router.get("/{product_id}", response_class=HTMLResponse)
def read_product_detail(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db)
):
    # Fetch the product
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Fetch similar products (e.g., same category or brand)
    recommended_products = get_similar_products(db, product)
    
    return render_frontend_template(
        "product_details.html",
        request,
        {
            "product": product,
            "recommended_products": recommended_products
        }
    )

