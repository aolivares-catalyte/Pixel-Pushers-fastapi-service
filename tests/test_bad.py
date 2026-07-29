from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_missing_unit_field_post():
    payload = {
        "name": "Basil Plant",
        "cost_per_unit": 5.0,
        "price_per_unit": 10.0,
        "quantity_in_stock": 100
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error = data["detail"][0]
    assert error["loc"] == ["body", "unit"]
    assert "field required" in error["msg"].lower()

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
    assert "greater than 0" in error["msg"].lower()

def test_bad_product_price():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": 1.75,
        "price_per_unit": 1.00,
        "quantity_in_stock": 38
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error = data["detail"][0]
    assert error["loc"] == ["body", "price_per_unit"]
    assert "greater than or equal to cost_per_unit" in error["msg"].lower()

def test_bad_product_quantity():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": 1.75,
        "price_per_unit": 4.99,
        "quantity_in_stock": -10
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error = data["detail"][0]
    assert error["loc"] == ["body", "quantity_in_stock"]
    assert "greater than or equal to 0" in error["msg"].lower()

def test_bad_product_cost_and_quantity():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": -1.75,
        "price_per_unit": 4.99,
        "quantity_in_stock": -38
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error_cost = data["detail"][0]
    assert error_cost["loc"] == ["body", "cost_per_unit"]
    assert "greater than 0" in error_cost["msg"]

    error_quantity = data["detail"][1]
    assert error_quantity["loc"] == ["body", "quantity_in_stock"]
    assert "greater than or equal to 0" in error_quantity["msg"]

def test_bad_product_price_and_quantity():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": 1.75,
        "price_per_unit": 1.00,
        "quantity_in_stock": -38
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error_price = data["detail"][0]
    assert error_price["loc"] == ["body", "price_per_unit"]
    assert "greater than or equal to cost_per_unit" in error_price["msg"]

    error_quantity = data["detail"][1]
    assert error_quantity["loc"] == ["body", "quantity_in_stock"]
    assert "greater than or equal to 0" in error_quantity["msg"]

def test_missing_search_parameter():
    response = client.get("/products/search")

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error = data["detail"][0]
    assert error["loc"] == ["query", "name"]
    assert "field required" in error["msg"].lower()

def test_bad_put_validation_quantity():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": 1.75,
        "price_per_unit": 1.00,
        "quantity_in_stock": -38
    }

    response = client.put("/products/1", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error_price = data["detail"][0]
    assert error_price["loc"] == ["body", "price_per_unit"]
    assert "greater than or equal to cost_per_unit" in error_price["msg"]

    error_quantity = data["detail"][1]
    assert error_quantity["loc"] == ["body", "quantity_in_stock"]
    assert "greater than or equal to 0" in error_quantity["msg"]

def test_bad_put_validation_cost():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": -1.75,
        "price_per_unit": 4.99,
        "quantity_in_stock": 38
    }

    response = client.put("/products/1", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error_cost = data["detail"][0]
    assert error_cost["loc"] == ["body", "cost_per_unit"]
    assert "greater than 0" in error_cost["msg"]

def test_bad_put_validation_price():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": 1.75,
        "price_per_unit": 1.00,
        "quantity_in_stock": 38
    }

    response = client.put("/products/1", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error_price = data["detail"][0]
    assert error_price["loc"] == ["body", "price_per_unit"]
    assert "greater than or equal to cost_per_unit" in error_price["msg"]

def test_bad_put_validation_cost_and_quantity():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": -1.75,
        "price_per_unit": 4.99,
        "quantity_in_stock": -38
    }

    response = client.put("/products/1", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error_cost = data["detail"][0]
    assert error_cost["loc"] == ["body", "cost_per_unit"]
    assert "greater than 0" in error_cost["msg"]

    error_quantity = data["detail"][1]
    assert error_quantity["loc"] == ["body", "quantity_in_stock"]
    assert "greater than or equal to 0" in error_quantity["msg"]

def test_bad_put_validation_price_and_quantity():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": 1.75,
        "price_per_unit": 1.00,
        "quantity_in_stock": -38
    }

    response = client.put("/products/1", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error_price = data["detail"][0]
    assert error_price["loc"] == ["body", "price_per_unit"]
    assert "greater than or equal to cost_per_unit" in error_price["msg"]

    error_quantity = data["detail"][1]
    assert error_quantity["loc"] == ["body", "quantity_in_stock"]
    assert "greater than or equal to 0" in error_quantity["msg"]

def test_bad_put_missing_unit():
    payload = {
        "name": "Basil Plant - 4in Pot",
        "cost_per_unit": 1.75,
        "price_per_unit": 4.99,
        "quantity_in_stock": 38
    }

    response = client.put("/products/1", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)

    error_unit = data["detail"][0]
    assert error_unit["loc"] == ["body", "unit"]
    assert "field required" in error_unit["msg"].lower()

def test_bad_patch_validation_price_and_quantity():
    payload = {
        "price_per_unit": 1.00,
        "quantity_in_stock": -38
    }

    response = client.patch("/products/1", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)

    errors = data["detail"]
    locs = [err["loc"][-1] for err in errors]

    # Only quantity_in_stock should fail
    assert "quantity_in_stock" in locs
    assert "price_per_unit" not in locs

    msgs = [err["msg"].lower() for err in errors]
    assert any("greater than or equal to 0" in msg for msg in msgs)


def test_bad_patch_validation_cost_and_quantity():
    payload = {
        "cost_per_unit": -1.75,
        "quantity_in_stock": -38
    }

    response = client.patch("/products/1", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)

    errors = data["detail"]
    locs = [err["loc"][-1] for err in errors]

    assert "cost_per_unit" in locs
    assert "quantity_in_stock" in locs

    msgs = [err["msg"].lower() for err in errors]

    assert any("greater than 0" in msg for msg in msgs)
    assert any("greater than or equal to 0" in msg for msg in msgs)
