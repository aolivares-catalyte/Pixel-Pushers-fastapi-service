"""Cross-feature tests validating category/product relationship behavior."""


def test_cross_category_reassignment_reflects_in_category_products(
    client,
    create_category,
    create_product,
) -> None:
    """Verify reassigned products move between category product lists."""
    primary_category = create_category(
        name="Cross Primary",
        description="Initial category for product",
    ).json()
    secondary_category = create_category(
        name="Cross Secondary",
        description="Target category for reassignment",
    ).json()

    created_product = create_product(
        name="Reassignable Product",
        category_id=primary_category["id"],
    ).json()

    move_response = client.patch(
        f"/products/{created_product['id']}",
        json={"category_id": secondary_category["id"]},
    )
    assert move_response.status_code == 200
    moved_product = move_response.json()
    assert moved_product["category_id"] == secondary_category["id"]

    first_category_products = client.get(
        f"/categories/{primary_category['id']}/products"
    ).json()["products"]
    second_category_products = client.get(
        f"/categories/{secondary_category['id']}/products"
    ).json()["products"]

    assert all(product["id"] != created_product["id"] for product in first_category_products)
    assert any(product["id"] == created_product["id"] for product in second_category_products)


def test_cross_create_products_in_two_categories_and_verify_grouping(
    client,
    create_category,
    create_product,
) -> None:
    """Verify products appear only in their assigned category collections."""
    herbs_category = create_category(
        name="Cross Herbs",
        description="Herb category",
    ).json()
    flowers_category = create_category(
        name="Cross Flowers",
        description="Flower category",
    ).json()

    herb_product = create_product(
        name="Cross Basil",
        category_id=herbs_category["id"],
    ).json()
    flower_product = create_product(
        name="Cross Marigold",
        category_id=flowers_category["id"],
    ).json()

    herbs_view = client.get(f"/categories/{herbs_category['id']}/products")
    flowers_view = client.get(f"/categories/{flowers_category['id']}/products")

    assert herbs_view.status_code == 200
    assert flowers_view.status_code == 200

    herbs_ids = [product["id"] for product in herbs_view.json()["products"]]
    flowers_ids = [product["id"] for product in flowers_view.json()["products"]]

    assert herb_product["id"] in herbs_ids
    assert flower_product["id"] in flowers_ids
    assert flower_product["id"] not in herbs_ids
    assert herb_product["id"] not in flowers_ids


def test_cross_put_product_with_valid_category_updates_relationship(
    client,
    create_category,
    create_product,
) -> None:
    """Verify a full product update can move category ownership."""
    source_category = create_category(
        name="Cross Put Source",
        description="Source category",
    ).json()
    target_category = create_category(
        name="Cross Put Target",
        description="Target category",
    ).json()

    product = create_product(
        name="Cross Put Product",
        category_id=source_category["id"],
    ).json()

    put_payload = {
        "name": "Cross Put Product Updated",
        "unit": "each",
        "cost_per_unit": 3.0,
        "price_per_unit": 6.0,
        "quantity_in_stock": 11,
        "category_id": target_category["id"],
    }
    put_response = client.put(f"/products/{product['id']}", json=put_payload)

    assert put_response.status_code == 200
    updated_product = put_response.json()
    assert updated_product["category_id"] == target_category["id"]

    source_products = client.get(f"/categories/{source_category['id']}/products").json()[
        "products"
    ]
    target_products = client.get(f"/categories/{target_category['id']}/products").json()[
        "products"
    ]

    assert all(item["id"] != product["id"] for item in source_products)
    assert any(item["id"] == product["id"] for item in target_products)
