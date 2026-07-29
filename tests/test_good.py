from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_product_happy_path():
    """
    Test 1: Happy-path create
    Proves that sending a valid payload successfully creates a product.
    """
    payload = {
        "name": "Monstera Deliciosa",
        "unit": "each",
        "cost_per_unit": 20.00,
        "price_per_unit": 45.99,
        "quantity_in_stock": 10,
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Monstera Deliciosa"
    assert data["cost_per_unit"] == 20.00
    assert data["price_per_unit"] == 45.99

    assert "id" in data
