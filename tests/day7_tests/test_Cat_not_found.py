from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_category_by_id_returns_404_for_missing_id():
    response = client.get("/categories/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category with ID 999999 not found."}


def test_get_category_products_returns_404_for_missing_id():
    response = client.get("/categories/999999/products")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category with ID 999999 not found."}
