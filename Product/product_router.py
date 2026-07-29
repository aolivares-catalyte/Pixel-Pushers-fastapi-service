from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from Product.product_model import Product
from utils import get_db

from Product.product_schema import *

# Create a router instance for product related endpoints
router = APIRouter()

# In memory list to store products
products_list = []


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product in the database.",
        )


@router.get("/", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all products currently stored in the database.
    Soft-deleted products are automatically excluded.
    """
    products = db.query(Product).filter(Product.is_deleted == False).all()
    if not products:
        return {"message": "No products found", "products": []}

    return {"message": "Products Found", "products": products}


@router.get(
    "/search", response_model=ProductListResponse, status_code=status.HTTP_200_OK
)
async def search_product(name: str, unit: str = "each", db: Session = Depends(get_db)):
    """
    Search for a product by name and unit in the database.
    Soft-deleted products are automatically excluded from results.

    Query parameters:
        name: The product name to search for.
        unit: Optional unit filter (defaults to "each").
    """

    products = (
        db.query(Product)
        .filter(Product.name == name, Product.unit == unit, Product.is_deleted == False)
        .all()
    )

    if products:
        return {"message": "Products Found", "products": products}
    return {"message": "No matching products found", "products": []}


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductRead,
)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its ID from the database.
    Returns 404 if the product does not exist or has been soft-deleted.
    """
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted == False)
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product

@router.put("/{product_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product_update: ProductFullUpdate,
    db: Session = Depends(get_db),
):
    """
    Fully update an existing product (full replacement).
    - Returns 404 if product is not found (not soft-deleted).
    - Only returns allowed fields (prevents SQLAlchemy leakage).
    - All update logic and DB commit is error-handled.
    """

    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted == False)
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product.name = product_update.name
    product.unit = product_update.unit
    product.cost_per_unit = product_update.cost_per_unit
    product.price_per_unit = product_update.price_per_unit
    product.quantity_in_stock = product_update.quantity_in_stock

    try:
        db.commit()
        db.refresh(product)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product in the database.",
        )

    return product


@router.patch(
    "/{product_id}", response_model=ProductRead, status_code=status.HTTP_200_OK
)
async def patch_product(
    product_id: int, product_update: ProductUpdatePartial, db: Session = Depends(get_db)
):
    """
    Update an existing product's details in the database.
    Returns 404 if the product does not exist or has been soft-deleted.
    """
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted == False)
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    try:
        ProductRead.model_validate(product)
    except ValidationError as e:
        db.rollback()
        raise RequestValidationError(e.errors())
    
    try:
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product in the database.",
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a product by setting its is_deleted flag to True.
    Returns 404 if the product does not exist or is already soft-deleted.
    """
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted == False)
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    try:
        product.is_deleted = True
        db.commit()
        db.refresh(product)
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product in the database.",
        )