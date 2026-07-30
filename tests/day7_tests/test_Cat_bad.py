from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


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
def test_bad_category_post_missing_name(payload):
    response = client.post("/categories/", json=payload)

    assert response.status_code == 422

    data = response.json()
    _assert_validation_response_shape(data)

    error = data["detail"][0]
    assert error["loc"] == ["body", "name"]
    assert "field required" in error["msg"].lower()
