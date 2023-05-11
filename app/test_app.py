import pytest
from flask import url_for
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Home Page" in response.data

def test_login(client):
    response = client.post("/login", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert b"Login successful" in response.data

def test_login_invalid_credentials(client):
    response = client.post("/login", json={"username": "invalid_user", "password": "invalid_password"})
    assert response.status_code == 401
    assert b"Invalid login credentials" in response.data

def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302  # Redirect status code

def test_info(client):
    response = client.get("/info")
    assert response.status_code == 200
    assert b"Information Page" in response.data

def test_info_id(client):
    response = client.get("/info/123")
    assert response.status_code == 200
    assert b"Information for ID 123" in response.data

def test_create_account(client):
    response = client.post("/createaccount", json={"username": "new_user", "password": "new_password"})
    assert response.status_code == 200
    assert b"Account Created" in response.data

def test_store(client):
    response = client.get("/store")
    assert response.status_code == 200
    assert b"Store Page" in response.data

def test_retrieve_product(client):
    response = client.get("/api/product/123")
    assert response.status_code == 200
    assert b"Product details for ID 123" in response.data

def test_remove_item(client):
    response = client.delete("/store/123")
    assert response.status_code == 200
    assert b"Product #123 removed successfully" in response.data

def test_create_product(client):
    response = client.post("/store/newproduct", json={"name": "New Product", "price": 10.0, "quantity": 5})
    assert response.status_code == 200
    assert b"Product #1 added successfully" in response.data

def test_update_product(client):
    response = client.put("/store/123", json={"name": "Updated Product", "price": 15.0, "quantity": 3})
    assert response.status_code == 200
    assert b"Product #123 updated successfully" in response.data

def test_admin_login(client):
    response = client.post("/admin", json={"username": "admin", "password": "admin_password"})
    assert response.status_code == 200
    assert b"Authentication successful" in response.data

def test_admin_store(client):
    response = client.get("/admin/store")
    assert response.status_code == 200
    assert b"Admin Store Page" in response.data

def test_unauthorized(client):
    response = client.get("/unauthorized")
    assert response.status_code == 200
    assert b"Unauthorized Access" in response.data

def test_product_store(client):
    response = client.get("/store/123")
    assert response.status_code == 200
    assert b"Store Page for Product ID 123" in response.data

def test_get_cache(client):
    response = client.get("/cache/example_url")
    assert response.status_code == 200
    assert b"Cache content for URL 'example_url'" in response.data