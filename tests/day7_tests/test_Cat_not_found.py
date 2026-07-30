def test_get_category_by_id_returns_404_for_missing_id(client):
    response = client.get("/categories/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category with ID 999999 not found."}


def test_get_category_products_returns_404_for_missing_id(client):
    response = client.get("/categories/999999/products")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category with ID 999999 not found."}


def test_put_category_returns_404_for_missing_id(client):
    payload = {
        "name": "Missing Category",
        "description": "Attempting to update category that does not exist",
    }
    response = client.put("/categories/999999", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Category with ID 999999 not found."}
