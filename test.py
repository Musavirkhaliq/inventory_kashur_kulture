# In a script or Python shell
from app.database import Base, engine
from app.models import Product, Sale, Restock, Invoice, Customer  # Import all models

# Drop all tables and recreate them
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)