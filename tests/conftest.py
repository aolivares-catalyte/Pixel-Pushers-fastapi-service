"""Shared pytest fixtures for API integration tests."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    """Provide a test client bound to the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def unique_suffix() -> str:
    """Return an 8-character random suffix for unique resource names."""
    return uuid4().hex[:8]


@pytest.fixture
def create_category(client: TestClient):
    """Return a helper that creates a category via the API."""

    def _create_category(
        name: str | None = None,
        description: str = "Test category",
    ):
        if name is None:
            name = f"Category-{uuid4().hex[:8]}"

        payload = {"name": name, "description": description}
        return client.post("/categories/", json=payload)

    return _create_category


@pytest.fixture
def create_product(client: TestClient):
    """Return a helper that creates a product via the API."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def _create_product(
        name: str | None = None,
        unit: str = "each",
        cost_per_unit: float = 2.0,
        price_per_unit: float = 4.0,
        quantity_in_stock: float = 10.0,
        category_id: int | None = None,
    ):
        if name is None:
            name = f"Product-{uuid4().hex[:8]}"

        payload = {
            "name": name,
            "unit": unit,
            "cost_per_unit": cost_per_unit,
            "price_per_unit": price_per_unit,
            "quantity_in_stock": quantity_in_stock,
        }
        if category_id is not None:
            payload["category_id"] = category_id

        return client.post("/products/", json=payload)

    return _create_product
