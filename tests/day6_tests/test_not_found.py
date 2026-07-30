def test_get_product_by_id_returns_404_for_missing_id(client):
    response = client.get("/products/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_put_returns_404_for_missing_product(client):
    payload = {
        "name": "Missing Product",
        "unit": "each",
        "cost_per_unit": 3.0,
        "price_per_unit": 7.0,
        "quantity_in_stock": 50,
    }
    response = client.put("/products/999999", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_patch_returns_404_for_missing_product(client):
    response = client.patch("/products/999999", json={"price_per_unit": 9.0})
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_create_product_returns_404_for_missing_category(client):
    payload = {
        "name": "Orphan Product",
        "unit": "each",
        "cost_per_unit": 4.0,
        "price_per_unit": 8.0,
        "quantity_in_stock": 10,
        "category_id": 999999,
    }
    response = client.post("/products/", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Category with ID 999999 not found."}
