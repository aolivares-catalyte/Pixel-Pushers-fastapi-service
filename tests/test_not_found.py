from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_product_by_id_returns_404_for_missing_id():
    response = client.get("/products/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}