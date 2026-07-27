from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from Product.product_model import Product
from utils import get_db

from Product.product_schema import *

# Create a router instance for product related endpoints
router = APIRouter()

# In memory list to store products
products_list = []


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Create a new product with the provided details.

    FastAPI automatically validates the incoming request body
    against ProductSchema. If validation fails (e.g., negative
    cost_per_unit or quantity_in_stock), FastAPI will return a 422
    response before this function is executed.
    """
    products_list.append(product)
    return product.model_dump()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_products():
    """
    Retrieve all products currently stored in memory.
    """
    return [product.model_dump() for product in products_list]


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_product(name: str, unit: str = "each"):
    """
    Search for a product by name and unit.

    Query parameters:
        name: The product name to search for.
        unit: Optional unit filter (defaults to "each").
    """
    return [
        product.model_dump()
        for product in products_list
        if product.name == name and product.unit == unit
    ]

@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductRead)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its ID from the database.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product