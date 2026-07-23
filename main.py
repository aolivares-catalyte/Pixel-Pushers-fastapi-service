"""
Main FastAPI application module.

This file initializes the FastAPI app, mounts the product router under the
`/products` prefix, and defines several top-level routes:

This module defines the application instance and two routes:
- ``GET /`` returns a default health-style greeting.
- ``GET /hello/{name}`` returns a personalized greeting.
- ``GET /db-check`` performs a simple database connectivity check by
  returning the number of rows in the ``products`` table.

A database session dependency is also defined here for use in top-level
endpoints.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from Product.models import Product
from Product.product_router import router as product_router

# Create the main FastAPI application instance
app = FastAPI()

# Mount product related routes under /products
app.include_router(product_router, prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """Return a default greeting message."""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def say_hello(name: str):
    """Return a greeting message addressed to the provided name."""
    return {"message": f"Hello, {name}!"}

@app.get("/db-check")
def check_database_connection(db: Session = Depends(get_db)):
    """
    Check database connectivity by returning the number of rows in
    the products table.
    """
    return {"row_count": db.query(Product).count()}

