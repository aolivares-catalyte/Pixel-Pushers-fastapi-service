from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_product_by_id_returns_404_for_missing_id():
    response = client.get("/products/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_put_updates_entire_product():
    create_payload = {
        "name": "Rose",
        "unit": "each",
        "cost_per_unit": 5.0,
        "price_per_unit": 10.0,
        "quantity_in_stock": 100
    }
    created = client.post("/products", json=create_payload).json()
    product_id = created["id"]

    update_payload = {
        "name": "Updated Rose",
        "unit": "each",
        "cost_per_unit": 6.0,
        "price_per_unit": 12.0,
        "quantity_in_stock": 200
    }
    response = client.put(f"/products/{product_id}", json=update_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Updated Rose"
    assert body["quantity_in_stock"] == 200

def test_patch_updates_partial_product():
    create_payload = {
        "name": "Tulip",
        "unit": "each",
        "cost_per_unit": 3.0,
        "price_per_unit": 7.0,
        "quantity_in_stock": 50
    }
    created = client.post("/products", json=create_payload).json()
    product_id = created["id"]

    patch_payload = {"price_per_unit": 9.0}
    response = client.patch(f"/products/{product_id}", json=patch_payload)

    assert response.status_code == 200
    body = response.json()

    assert body["price_per_unit"] == 9.0

    assert body["name"] == "Tulip"
    assert body["cost_per_unit"] == 3.0
    assert body["quantity_in_stock"] == 50
