from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def unique_suffix():
    return uuid4().hex[:8]


@pytest.fixture
def create_category(client):
    def _create_category(name: str | None = None, description: str = "Test category"):
        if name is None:
            name = f"Category-{uuid4().hex[:8]}"

        payload = {"name": name, "description": description}
        response = client.post("/categories/", json=payload)
        return response

    return _create_category


@pytest.fixture
def create_product(client):
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

        response = client.post("/products/", json=payload)
        return response

    return _create_product