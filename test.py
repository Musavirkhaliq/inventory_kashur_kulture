from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    # Simulating a response
    print(product)
    return product  # Ensure the returned data matches the Product schema
