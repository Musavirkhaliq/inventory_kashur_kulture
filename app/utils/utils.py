# Helper function for rendering templates 
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
# Initialize templates
templates = Jinja2Templates(directory="templates")
frontend_templates = Jinja2Templates(directory="frontend/templates")

def render_template(template_name: str, request, context: dict = {}):
    context["request"] = request
    return templates.TemplateResponse(template_name, context)

def render_frontend_template(template_name: str, request, context: dict = {}):
    context["request"] = request
    return frontend_templates.TemplateResponse(template_name, context)



# Password hashing utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)