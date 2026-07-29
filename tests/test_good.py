from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_product_happy_path():
    """
    Test 1: Happy-path create
    Proves that sending a valid payload successfully creates a product.
    """
    payload = {
        "name": "Cherry Tomatoes - 1lb Clamshell",
        "unit": "lb",
        "cost_per_unit": 1.10,
        "price_per_unit": 3.49,
        "quantity_in_stock": 52,
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Cherry Tomatoes - 1lb Clamshell"
    assert data["cost_per_unit"] == 1.10
    assert data["price_per_unit"] == 3.49

    assert "id" in data
