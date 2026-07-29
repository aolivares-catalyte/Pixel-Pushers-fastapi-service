from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """Test the default health-style greeting."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_db_check():
    """Test the database connectivity endpoint."""
    response = client.get("/db-check")
    assert response.status_code == 200
    assert "row_count" in response.json()


def test_create_product_validation_failure():
    """
    Test 2: Bad path / Validation failure.
    Proves that sending invalid data (negative cost) is rejected by Pydantic.
    """
    payload = {
        "name": "Invalid Tomato",
        "unit": "each",
        "cost_per_unit": -5.00,
        "price_per_unit": 3.00,
        "quantity_in_stock": 10,
    }
    response = client.post("/products/", json=payload)

    assert response.status_code == 422


def test_get_product_not_found():
    """
    Test 3: Not-found case.
    Proves that requesting a non-existent product returns a 404.
    """
    response = client.get("/products/9999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_full_product_lifecycle():
    """
    Tests the complete lifecycle of a product to avoid database state issues.
    Covers POST, GET, PUT, PATCH, and DELETE in one isolated flow.
    """

    payload = {
        "name": "Test Lifecycle Plant",
        "unit": "each",
        "cost_per_unit": 5.00,
        "price_per_unit": 10.00,
        "quantity_in_stock": 20,
    }
    create_res = client.post("/products/", json=payload)
    assert create_res.status_code == 201
    product_id = create_res.json()["id"]

    get_res = client.get(f"/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Test Lifecycle Plant"

    search_res = client.get(f"/products/search?name=Test Lifecycle Plant&unit=each")
    assert search_res.status_code == 200
    assert len(search_res.json()["products"]) > 0

    put_payload = payload.copy()
    put_payload["name"] = "Updated Lifecycle Plant"
    put_res = client.put(f"/products/{product_id}", json=put_payload)
    assert put_res.status_code == 200
    assert put_res.json()["name"] == "Updated Lifecycle Plant"

    patch_payload = {"quantity_in_stock": 15}
    patch_res = client.patch(f"/products/{product_id}", json=patch_payload)
    assert patch_res.status_code == 200
    assert patch_res.json()["quantity_in_stock"] == 15

    delete_res = client.delete(f"/products/{product_id}")
    assert delete_res.status_code == 204

    get_deleted_res = client.get(f"/products/{product_id}")
    assert get_deleted_res.status_code == 404
