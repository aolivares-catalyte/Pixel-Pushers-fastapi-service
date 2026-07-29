from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_bad_product_cost():
    payload = {
        "name": "Basil Plant",
        "unit": "each",
        "cost_per_unit": -5.0,
        "price_per_unit": 10.0,
        "quantity_in_stock": 100
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error = data["detail"][0]
    assert error["loc"] == ["body", "cost_per_unit"]
    assert "greater than 0" in error["msg"]