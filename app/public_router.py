from fastapi import APIRouter
from app.api.public.products.router import router as public_products_router 
from app.api.public.cart.router import router as public_cart_router



# router = APIRouter(prefix="/api")
router = APIRouter()  # No prefix

router.include_router(public_products_router)
router.include_router(public_cart_router)
