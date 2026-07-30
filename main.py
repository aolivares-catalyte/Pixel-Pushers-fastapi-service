"""Main FastAPI application entry point.

This module wires routers, initializes database metadata, and exposes
lightweight endpoints used by tests and quick health checks.
"""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from Category import category_model
from Category.category_router import router as category_router
from Product import product_model
from Product.product_router import router as product_router
from database import Base, engine
from utils import get_db

# Keep model modules imported so SQLAlchemy metadata contains all tables.
_MODELS_REGISTERED = (product_model, category_model)

app = FastAPI()

app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(category_router, prefix="/categories", tags=["categories"])

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a default greeting message."""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def say_hello(name: str) -> dict[str, str]:
    """Return a greeting addressed to the supplied name."""
    return {"message": f"Hello, {name}!"}


@app.get("/db-check")
def check_database_connection(db: Session = Depends(get_db)) -> dict[str, int]:
    """Return row count from the products table to verify DB connectivity."""
    return {"row_count": db.query(product_model.Product).count()}
