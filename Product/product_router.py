from fastapi import APIRouter, status
from Product.product_model import Product
from fastapi import Depends
from sqlalchemy.orm import Session
from utils import get_db

from Product.product_schema import ProductSchema

# Create a router instance for product related endpoints
router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    """
    Create a new product with the provided details.

    FastAPI automatically validates the incoming request body
    against ProductSchema. If validation fails (e.g., negative
    cost_per_unit or quantity_in_stock), FastAPI will return a 422
    response before this function is executed.
    """
    db_product = Product(
        name=product.name,
        unit=product.unit,
        cost_per_unit=product.cost_per_unit,
        price_per_unit=product.price_per_unit,
        quantity_in_stock=product.quantity_in_stock,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", status_code=status.HTTP_200_OK)
async def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all products currently stored in the database.
    """
    return db.query(Product).all()


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_product(name: str, unit: str = "each", db: Session = Depends(get_db)):
    """
    Search for a product by name and unit.

    Query parameters:
        name: The product name to search for.
        unit: Optional unit filter (defaults to "each").
    """
    return db.query(Product).filter(Product.name == name, Product.unit == unit).all()
