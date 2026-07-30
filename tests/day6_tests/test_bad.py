"""Negative-path validation tests for product endpoints."""

import pytest


def _assert_validation_response_shape(data: dict) -> None:
    """Assert that validation responses include the FastAPI detail list."""
    assert "detail" in data
    assert isinstance(data["detail"], list)


def _assert_error_by_field(
    errors: list[dict],
    field: str,
    message_substring: str,
) -> None:
    """Assert that validation errors include an expected field/message match."""
    field_errors = [error for error in errors if error["loc"][-1] == field]
    assert field_errors, f"No validation error found for field '{field}'"
    assert any(message_substring in error["msg"].lower() for error in field_errors)


@pytest.mark.parametrize(
    "payload, expected_field, expected_message",
    [
        (
            {
                "name": "Basil Plant",
                "cost_per_unit": 5.0,
                "price_per_unit": 10.0,
                "quantity_in_stock": 100,
            },
            "unit",
            "field required",
        ),
        (
            {
                "name": "Basil Plant",
                "unit": "each",
                "cost_per_unit": -5.0,
                "price_per_unit": 10.0,
                "quantity_in_stock": 100,
            },
            "cost_per_unit",
            "greater than 0",
        ),
        (
            {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": 1.75,
                "price_per_unit": 1.00,
                "quantity_in_stock": 38,
            },
            "price_per_unit",
            "greater than or equal to cost_per_unit",
        ),
        (
            {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": 1.75,
                "price_per_unit": 4.99,
                "quantity_in_stock": -10,
            },
            "quantity_in_stock",
            "greater than or equal to 0",
        ),
    ],
    ids=["missing-unit", "bad-cost", "bad-price", "bad-quantity"],
)
def test_bad_product_post_single_error(
    client,
    payload: dict,
    expected_field: str,
    expected_message: str,
) -> None:
    """Verify each invalid POST payload returns the expected single validation error."""
    response = client.post("/products/", json=payload)
    assert response.status_code == 422

    data = response.json()
    _assert_validation_response_shape(data)
    _assert_error_by_field(data["detail"], expected_field, expected_message)


@pytest.mark.parametrize(
    "payload, expected_errors",
    [
        (
            {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": -1.75,
                "price_per_unit": 4.99,
                "quantity_in_stock": -38,
            },
            [
                ("cost_per_unit", "greater than 0"),
                ("quantity_in_stock", "greater than or equal to 0"),
            ],
        ),
        (
            {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": 1.75,
                "price_per_unit": 1.00,
                "quantity_in_stock": -38,
            },
            [
                ("price_per_unit", "greater than or equal to cost_per_unit"),
                ("quantity_in_stock", "greater than or equal to 0"),
            ],
        ),
    ],
    ids=["bad-cost-and-quantity", "bad-price-and-quantity"],
)
def test_bad_product_post_multi_error(
    client,
    payload: dict,
    expected_errors: list[tuple[str, str]],
) -> None:
    """Verify POST payloads with multiple issues report all expected errors."""
    response = client.post("/products/", json=payload)
    assert response.status_code == 422

    data = response.json()
    _assert_validation_response_shape(data)

    for field, message in expected_errors:
        _assert_error_by_field(data["detail"], field, message)


def test_missing_search_parameter(client) -> None:
    """Verify product search without name query parameter returns 422."""
    response = client.get("/products/search")

    assert response.status_code == 422

    data = response.json()
    _assert_validation_response_shape(data)

    error = data["detail"][0]
    assert error["loc"] == ["query", "name"]
    assert "field required" in error["msg"].lower()


@pytest.mark.parametrize(
    "payload, expected_errors",
    [
        (
            {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": -1.75,
                "price_per_unit": 4.99,
                "quantity_in_stock": 38,
            },
            [("cost_per_unit", "greater than 0")],
        ),
        (
            {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": 1.75,
                "price_per_unit": 1.00,
                "quantity_in_stock": 38,
            },
            [("price_per_unit", "greater than or equal to cost_per_unit")],
        ),
        (
            {
                "name": "Basil Plant - 4in Pot",
                "cost_per_unit": 1.75,
                "price_per_unit": 4.99,
                "quantity_in_stock": 38,
            },
            [("unit", "field required")],
        ),
        (
            {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": -1.75,
                "price_per_unit": 4.99,
                "quantity_in_stock": -38,
            },
            [
                ("cost_per_unit", "greater than 0"),
                ("quantity_in_stock", "greater than or equal to 0"),
            ],
        ),
        (
            {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": 1.75,
                "price_per_unit": 1.00,
                "quantity_in_stock": -38,
            },
            [
                ("price_per_unit", "greater than or equal to cost_per_unit"),
                ("quantity_in_stock", "greater than or equal to 0"),
            ],
        ),
    ],
    ids=[
        "bad-cost",
        "bad-price",
        "missing-unit",
        "bad-cost-and-quantity",
        "bad-price-and-quantity",
    ],
)
def test_bad_put_validation(
    client,
    payload: dict,
    expected_errors: list[tuple[str, str]],
) -> None:
    """Verify full-update payload validation failures return precise PUT errors."""
    response = client.put("/products/1", json=payload)
    assert response.status_code == 422

    data = response.json()
    _assert_validation_response_shape(data)

    for field, message in expected_errors:
        _assert_error_by_field(data["detail"], field, message)


@pytest.mark.parametrize(
    "payload, expected_present_fields, expected_absent_fields, expected_messages",
    [
        (
            {"price_per_unit": 1.00, "quantity_in_stock": -38},
            ["quantity_in_stock"],
            ["price_per_unit"],
            ["greater than or equal to 0"],
        ),
        (
            {"cost_per_unit": -1.75, "quantity_in_stock": -38},
            ["cost_per_unit", "quantity_in_stock"],
            [],
            ["greater than 0", "greater than or equal to 0"],
        ),
    ],
    ids=["bad-price-and-quantity", "bad-cost-and-quantity"],
)
def test_bad_patch_validation(
    client,
    payload: dict,
    expected_present_fields: list[str],
    expected_absent_fields: list[str],
    expected_messages: list[str],
) -> None:
    """Verify partial-update validation behavior for PATCH requests."""
    response = client.patch("/products/1", json=payload)
    assert response.status_code == 422

    data = response.json()
    _assert_validation_response_shape(data)

    errors = data["detail"]
    locs = [error["loc"][-1] for error in errors]

    for field in expected_present_fields:
        assert field in locs

    for field in expected_absent_fields:
        assert field not in locs

    for message in expected_messages:
        assert any(message in error["msg"].lower() for error in errors)
