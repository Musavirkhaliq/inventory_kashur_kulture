from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Get the current directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount static files and templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/products")
async def products(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return templates.TemplateResponse("products.html", {
        "request": request,
        "products": products
    })

@app.post("/api/products")
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/api/products")
async def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)