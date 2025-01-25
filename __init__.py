from app.database import Base, engine
from app.models import Product, Sale, Restock, Invoice

# Drop all tables and recreate them
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)