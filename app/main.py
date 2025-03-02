from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .api_router import router as api_router
from app.utils.utils import render_template

# Import database
from . import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Root Endpoint
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request): 
    return render_template("index.html", request)


app.include_router(api_router)