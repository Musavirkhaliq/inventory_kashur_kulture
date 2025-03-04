from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .web_routers import router as web_routers
from .api_router import router as api_router
from app.utils.utils import render_template,render_frontend_template
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
# Initialize templates

# Import database
from . import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root Endpoint
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request): 
    return render_frontend_template("/login.html", request)

# This index.html is in frontedn --> templates
@app.get("/kashur_kulture", response_class=HTMLResponse)
def read_root(request: Request): 
    return render_frontend_template("/index.html", request)


# Type this in the pannel to access the admin page. This index.html is in templates
@app.get("/admin", response_class=HTMLResponse)
def read_root(request: Request): 
    return render_template("/index.html", request)

app.include_router(api_router)
app.include_router(web_routers)