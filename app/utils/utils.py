# Helper function for rendering templates 
from fastapi.templating import Jinja2Templates
# Initialize templates
templates = Jinja2Templates(directory="templates")

def render_template(template_name: str, request, context: dict = {}):
    context["request"] = request
    return templates.TemplateResponse(template_name, context)
