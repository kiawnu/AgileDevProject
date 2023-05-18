import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app
from database.database import db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    client = app.test_client()


    yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Gardenia' in response.data.decode('utf-8')


def test_login(client):
    response = client.post('/login', json={"username": "username", "password": "password"})
    assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200
    assert 'Unauthorized' in response.data.decode('utf-8')


def test_info(client):
    response = client.get('/info')
    assert response.status_code == 200


def test_info_id(client):
    response = client.get('/info/1')
    assert response.status_code == 200

def test_store(client):
    response = client.get('/store')
    assert response.status_code == 200

# def test_get_product(client):
#     response = client.get('api/product/3')
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "id": 3,
#         "img": "https://perenual.com/storage/species_image/3_abies_concolor/regular/52292935430_f4f3b22614_b.jpg",
#         "name": "White Fir",
#         "price": 19.99,
#         "quantity": 15,
#         "sname": "Abies concolor"
#     }


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
