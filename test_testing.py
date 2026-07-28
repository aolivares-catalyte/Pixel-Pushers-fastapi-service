import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_delete_product_by_id_success():
    """
    Verify that providing a valid product_id returns 200 OK 
    and soft-deletes the item (is_active = False).
    """
    # 1. Arrange: Pick an ID of a product that exists in your database
    target_id = 1

    # 2. Act: Send a DELETE request with query parameters: /products/?product_id=1
    response = client.delete(f"/products/?product_id={target_id}")

    # 3. Assert: Check that the API responded with 200 OK and expected JSON
    assert response.status_code == 200
    
    response_data = response.json()
    assert response_data["status"] == "success"
    assert response_data["is_active"] == False

def test_delete_product_by_name_success():
 """
 Verify that providing a valid product name returns 200 OK 
    and soft-deletes the item.
    """
    # Act: Send DELETE /products/?name=Monstera
response = client.delete("/products/?name=Monstera")

    # Assert
assert response.status_code == 200
    
response_data = response.json()
assert response_data["status"] == "success"
assert response_data["is_active"] == False

def test_delete_product_not_found():
    """
    Verify that attempting to delete a non-existent product 
    returns a 404 status code and a clear error message.
    """
    # Act: Pass an ID that definitely does not exist in the DB
    response = client.delete("/products/?product_id=999999")

    # Assert
    assert response.status_code == 404
    
    response_data = response.json()
    # Check that our friendly error detail is returned!
    assert "Cannot delete product. No product found" in response_data["detail"]

def test_delete_product_missing_all_parameters():
    """
    Verify that sending a DELETE request without 'product_id' or 'name' 
    returns a 400 Bad Request error.
    """
    # Act: Send empty query params
    response = client.delete("/products/")

    # Assert
    assert response.status_code == 400
    
    response_data = response.json()
    assert "You must supply either 'product_id' or 'name'" in response_data["detail"]

    