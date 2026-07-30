import pytest


def _assert_validation_response_shape(data):
    assert "detail" in data
    assert isinstance(data["detail"], list)


@pytest.mark.parametrize(
    "payload",
    [
        {"description": "Missing name field"},
    ],
    ids=["missing-name"],
)
def test_bad_category_post_missing_name(client, payload):
    response = client.post("/categories/", json=payload)

    assert response.status_code == 422

    data = response.json()
    _assert_validation_response_shape(data)

    error = data["detail"][0]
    assert error["loc"] == ["body", "name"]
    assert "field required" in error["msg"].lower()


def test_product_put_returns_404_for_missing_category(client, create_product):
    product_response = create_product(name="Put Invalid Category")
    product_id = product_response.json()["id"]

    put_payload = {
        "name": "Put Invalid Category Updated",
        "unit": "each",
        "cost_per_unit": 2.0,
        "price_per_unit": 4.0,
        "quantity_in_stock": 10,
        "category_id": 999999,
    }
    response = client.put(f"/products/{product_id}", json=put_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Category with ID 999999 not found."}


def test_product_patch_returns_404_for_missing_category(client, create_product):
    product_response = create_product(name="Patch Invalid Category")
    product_id = product_response.json()["id"]

    response = client.patch(f"/products/{product_id}", json={"category_id": 999999})
    assert response.status_code == 404
    assert response.json() == {"detail": "Category with ID 999999 not found."}
