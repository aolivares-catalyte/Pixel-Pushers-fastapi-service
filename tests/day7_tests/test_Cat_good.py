def test_create_category(client):
    payload = {
        "name": "Garden Supplies",
        "description": "Tools and supplies for gardening",
    }
    response = client.post("/categories/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["description"] == payload["description"]


def test_get_category_by_id(client):
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


def test_get_categories_returns_list_shape(client, create_category):
    create_category(name="List Category A", description="First list category")
    create_category(name="List Category B", description="Second list category")

    response = client.get("/categories/")
    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert "categories" in body
    assert isinstance(body["categories"], list)


def test_get_category_products_returns_nested_products(
    client, create_category, create_product
):
    category_response = create_category(
        name="Herbs Nest", description="Fresh herbs for cooking"
    )
    category = category_response.json()

    product_response = create_product(
        name="Nested Basil",
        unit="each",
        cost_per_unit=2.0,
        price_per_unit=4.0,
        quantity_in_stock=12,
        category_id=category["id"],
    )
    created_product = product_response.json()

    response = client.get(f"/categories/{category['id']}/products")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == category["id"]
    assert body["name"] == category["name"]
    assert isinstance(body["products"], list)
    assert any(product["id"] == created_product["id"] for product in body["products"])
