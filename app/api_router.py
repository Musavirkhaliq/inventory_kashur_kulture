from fastapi import APIRouter
from .customers.router import router as customers_router
from .products.router import router as products_router
from .sales.router import router as sales_router
from .restock.router import router as restock_router
from .invoices.router import router as invoices_router
from .users.routers import router as users_router
from .auth.router import router as auth_router

# router = APIRouter(prefix="/api")
router = APIRouter()  # No prefix

router.include_router(customers_router)
router.include_router(products_router)
router.include_router(sales_router)
router.include_router(restock_router)
router.include_router(invoices_router)
router.include_router(users_router)
router.include_router(auth_router)

