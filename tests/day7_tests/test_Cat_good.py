from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_category():
    payload = {
        "name": "Garden Supplies",
        "description": "Tools and supplies for gardening",
    }
    response = client.post("/categories/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["description"] == payload["description"]


def test_get_category_by_id():
    payload = {
        "name": "Indoor Plants",
        "description": "Plants that thrive indoors",
    }
    created = client.post("/categories/", json=payload).json()

    response = client.get(f"/categories/{created['id']}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created["id"]
    assert body["name"] == payload["name"]
    assert body["description"] == payload["description"]


def test_get_category_products_returns_nested_products():
    category_payload = {
        "name": "Herbs",
        "description": "Fresh herbs for cooking",
    }
    category = client.post("/categories/", json=category_payload).json()

    product_payload = {
        "name": "Basil",
        "unit": "each",
        "cost_per_unit": 2.0,
        "price_per_unit": 4.0,
        "quantity_in_stock": 12,
        "category_id": category["id"],
    }
    created_product = client.post("/products/", json=product_payload).json()

    response = client.get(f"/categories/{category['id']}/products")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == category["id"]
    assert any(product["id"] == created_product["id"] for product in body["products"])
