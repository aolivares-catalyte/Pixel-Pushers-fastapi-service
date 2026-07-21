"""FastAPI service entry point for basic greeting endpoints.

This module defines the application instance and two routes:
- ``GET /`` returns a default health-style greeting.
- ``GET /hello/{name}`` returns a personalized greeting.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Return a default greeting message."""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def say_hello(name: str):
    """Return a greeting message addressed to the provided name."""
    return {"message": f"Hello, {name}!"}
