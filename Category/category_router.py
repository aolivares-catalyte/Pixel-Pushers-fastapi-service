"""FastAPI routes for category CRUD and category-product views."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from Category.category_model import Category
from Category.category_schema import (
    CategoryCreate,
    CategoryListResponse,
    CategoryRead,
    CategoryReadWithProducts,
)
from utils import get_db

router = APIRouter()


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryRead:
    """Create a category and return the persisted entity."""
    new_category = Category(**category.model_dump())
    db.add(new_category)

    try:
        db.commit()
        db.refresh(new_category)
        return new_category
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create category in the database.",
        ) from exc


@router.get("/", response_model=CategoryListResponse, status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db)) -> CategoryListResponse:
    """Return all categories or an empty response payload."""
    categories = db.query(Category).all()
    if not categories:
        return {"message": "No categories found", "categories": []}

    return {"message": "Categories Found", "categories": categories}


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
)
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryRead:
    """Return one category by identifier."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found.",
        )
    return category


@router.get(
    "/{category_id}/products",
    response_model=CategoryReadWithProducts,
    status_code=status.HTTP_200_OK,
)
def get_category_with_products(
    category_id: int,
    db: Session = Depends(get_db),
) -> CategoryReadWithProducts:
    """Return a category and its related products by category id."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found.",
        )
    return category


@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
)
def update_category(
    category_id: int,
    category_update: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryRead:
    """Replace an existing category with the supplied payload."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found.",
        )

    for key, value in category_update.model_dump().items():
        setattr(category, key, value)

    try:
        db.commit()
        db.refresh(category)
        return category
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update category in the database.",
        ) from exc
