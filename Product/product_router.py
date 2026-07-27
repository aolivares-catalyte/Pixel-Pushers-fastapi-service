from fastapi import APIRouter, status, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from Product.product_schema import ProductSchema

# Create a router instance for product related endpoints
router = APIRouter()

# In memory list to store products
products_list = []


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    """
    Create a new product with the provided details and persist it to the database.

    FastAPI automatically validates the incoming request body
    against ProductSchema. If validation fails (e.g., negative
    cost_per_unit or quantity_in_stock), FastAPI will return a 422
    response before this function is executed.
    """
    new_product = Product(**product.model_dump())
    db.add(new_product)

    try:

        db.commit()

        db.refresh(new_product)
        return new_product

    except Exception as e:

        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create product in the database.",
        )


@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all products currently stored in the database.
    """

    products = db.query(Product).all()

    return products


@router.get("/search", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
def search_product(name: str, unit: str = "each", db: Session = Depends(get_db)):
    """
    Search for a product by name and unit in the database.

    Query parameters:
        name: The product name to search for.
        unit: Optional unit filter (defaults to "each").
    """

    products = (
        db.query(Product).filter(Product.name == name, Product.unit == unit).all()
    )

    return products


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchema,
)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its ID from the database.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product
