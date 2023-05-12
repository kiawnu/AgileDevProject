import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.app import app
from database.database import db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login(client):
    response = client.post('/login', json={"username": "test", "password": "password"})
    assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302


def test_info(client):
    response = client.get('/info')
    assert response.status_code == 200


def test_info_id(client):
    response = client.get('/info/1')
    assert response.status_code == 200


def test_create_account(client):
    response = client.post('/createaccount', json={"username": "test", "password": "password"})
    assert response.status_code == 200


def test_store(client):
    response = client.get('/store')
    assert response.status_code == 200


def test_retrieve_product(client):
    response = client.get('/api/product/1')
    assert response.status_code == 200


def test_remove_item(client):
    response = client.delete('/store/1')
    assert response.status_code == 200


def test_create_product(client):
    response = client.post('/store/newproduct', json={"name": "Test Product", "price": 10, "quantity": 5})
    assert response.status_code == 200


def test_update_product(client):
    response = client.put('/store/1', json={"name": "Updated Product", "price": 20, "quantity": 10})
    assert response.status_code == 200


def test_admin(client):
    response = client.post('/admin', json={"username": "admin", "password": "admin"})
    assert response.status_code == 200


def test_admin_store(client):
    response = client.get('/admin/store')
    assert response.status_code == 200


def test_unauthorized(client):
    response = client.get('/unauthorized')
    assert response.status_code == 200


def test_get_products(client):
    response = client.get('/api/products')
    assert response.status_code == 200


def test_product_store(client):
    response = client.get('/store/1')
    assert response.status_code == 200


def test_get_cache(client):
    response = client.get('/cache/test_url')
    assert response.status_code == 400


def test_put_cache(client):
    response = client.put('/cache/test_url', json={"data": "test_data"})
    assert response.status_code == 200