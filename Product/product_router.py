"""FastAPI routes for product CRUD, search, and soft-delete behavior."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from Category.category_model import Category
from Product.product_model import Product
from Product.product_schema import (
    ProductCreate,
    ProductFullUpdate,
    ProductListResponse,
    ProductRead,
    ProductUpdatePartial,
)
from utils import get_db

router = APIRouter()


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)) -> ProductRead:
    """Create a product after validating any supplied category reference."""
    new_product = Product(**product.model_dump())
    db.add(new_product)

    if new_product.category_id is not None:
        category = (
            db.query(Category).filter(Category.id == new_product.category_id).first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {new_product.category_id} not found.",
            )

    try:
        db.commit()
        db.refresh(new_product)
        return new_product
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category with ID {new_product.category_id} does not exist.",
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product in the database.",
        ) from exc


@router.get("/", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def get_products(db: Session = Depends(get_db)) -> ProductListResponse:
    """Return all non-deleted products."""
    products = db.query(Product).filter(Product.is_deleted.is_(False)).all()
    if not products:
        return {"message": "No products found", "products": []}

    return {"message": "Products Found", "products": products}


@router.get("/search", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def search_product(
    name: str,
    unit: str = "each",
    db: Session = Depends(get_db),
) -> ProductListResponse:
    """Search non-deleted products by exact name and unit."""
    products = (
        db.query(Product)
        .filter(
            Product.name == name,
            Product.unit == unit,
            Product.is_deleted.is_(False),
        )
        .all()
    )

    if products:
        return {"message": "Products Found", "products": products}
    return {"message": "No matching products found", "products": []}


@router.get("/{product_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
) -> ProductRead:
    """Return one non-deleted product by id or raise 404."""
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted.is_(False))
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.put("/{product_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product_update: ProductFullUpdate,
    db: Session = Depends(get_db),
) -> ProductRead:
    """Fully replace a non-deleted product with the provided payload."""
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted.is_(False))
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    product.name = product_update.name
    product.unit = product_update.unit
    product.cost_per_unit = product_update.cost_per_unit
    product.price_per_unit = product_update.price_per_unit
    product.quantity_in_stock = product_update.quantity_in_stock
    product.category_id = product_update.category_id

    if product_update.category_id is not None:
        category = (
            db.query(Category).filter(Category.id == product_update.category_id).first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {product_update.category_id} not found.",
            )

    try:
        db.commit()
        db.refresh(product)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Foreign key constraint violated: invalid category_id.",
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product in the database.",
        ) from exc

    return product


@router.patch("/{product_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def patch_product(
    product_id: int,
    product_update: ProductUpdatePartial,
    db: Session = Depends(get_db),
) -> ProductRead:
    """Partially update a non-deleted product and validate result."""
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted.is_(False))
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    try:
        ProductRead.model_validate(product)
    except ValidationError as exc:
        db.rollback()
        raise RequestValidationError(exc.errors()) from exc

    if product_update.category_id is not None:
        category = (
            db.query(Category).filter(Category.id == product_update.category_id).first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {product_update.category_id} not found.",
            )

    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Foreign key constraint violated: invalid category_id.",
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product in the database.",
        ) from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    """Soft-delete a product by setting its deletion flag."""
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted.is_(False))
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    try:
        product.is_deleted = True
        db.commit()
        db.refresh(product)
        return None
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product in the database.",
        ) from exc
