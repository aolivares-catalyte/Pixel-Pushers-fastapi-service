"""
FastAPI service entry point for basic greeting endpoints.

This module defines the application instance and two routes:
- ``GET /`` returns a default health-style greeting.
- ``GET /hello/{name}`` returns a personalized greeting.

It also mounts the product router under the /products prefix.
"""

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from Product.product_router import router as product_router

# Create the main FastAPI application instance
app = FastAPI()

# Mount product related routes under /products
app.include_router(product_router, prefix="/products", tags=["products"])

@app.get("/")
def read_root():
    """Return a default greeting message."""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def say_hello(name: str):
    """Return a greeting message addressed to the provided name."""
    return {"message": f"Hello, {name}!"}

