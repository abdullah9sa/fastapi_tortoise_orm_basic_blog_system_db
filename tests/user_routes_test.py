from fastapi import APIRouter, HTTPException
from fastapi.testclient import TestClient

# Define test cases for your routes
def test_get_user(client):
    response = client.get("/users/100")
    assert response.status_code == 404  # Assuming user with ID 100 doesn't exist

