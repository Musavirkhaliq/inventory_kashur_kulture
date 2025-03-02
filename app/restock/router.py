from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.products.services import get_all_products
from app.restock.schemas import Restock, RestockCreate
from app.restock.services import get_all_restocks, create_restock

from app.utils.utils import render_template

router = APIRouter(prefix="/restocks", tags=["restocks"])

@router.get("/", response_class=HTMLResponse)
def read_restocks(request: Request, db: Session = Depends(get_db)):
    restocks = get_all_restocks(db)
    products = get_all_products(db)
    return render_template("restocks.html", request, {
        "restocks": restocks,
        "products": products
    })

@router.post("/", response_model=Restock)
def create_restock(restock: RestockCreate, db: Session = Depends(get_db)):
    try:
        return create_restock(db, restock)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))