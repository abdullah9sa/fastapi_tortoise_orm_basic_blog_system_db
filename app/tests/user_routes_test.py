from fastapi import APIRouter, HTTPException
from fastapi.testclient import TestClient
import bcrypt
from app.models.user import *
from app.main import app 

router = APIRouter()
client = TestClient(app)  # Create a TestClient instance

# test cases
def test_get_user():
    response = client.get("/users/{user_id}", json={"user_id": 1})
    assert response.status_code == 404  # Assuming user with ID 1 doesn't exist

def test_register_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "join_date" in data

# Run tests
if __name__ == "__main__":
    test_get_user()
    test_register_user()
