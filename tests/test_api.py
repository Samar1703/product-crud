import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import crud

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset():
    crud.reset_store()

def test_create_product_api():
    response = client.post('/products', json={
        'nom': 'Stylo', 'description': 'Stylo bleu', 'prix': 1.5, 'quantite_stock': 100
    })
    assert response.status_code == 201
    assert response.json()['nom'] == 'Stylo'

def test_list_products_api():
    client.post('/products', json={'nom': 'P1', 'description': 'd1', 'prix': 1.0, 'quantite_stock': 10})
    client.post('/products', json={'nom': 'P2', 'description': 'd2', 'prix': 2.0, 'quantite_stock': 20})
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_product_api():
    created = client.post('/products', json={
        'nom': 'Cahier', 'description': 'Cahier A4', 'prix': 3.0, 'quantite_stock': 50
    }).json()
    product_id = created['id']
    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.json()['nom'] == 'Cahier'

def test_get_product_not_found_api():
    response = client.get('/products/999')
    assert response.status_code == 404

def test_update_product_api():
    created = client.post('/products', json={
        'nom': 'Crayon', 'description': 'Crayon HB', 'prix': 0.5, 'quantite_stock': 200
    }).json()
    product_id = created['id']
    response = client.put(f'/products/{product_id}', json={'prix': 0.9})
    assert response.status_code == 200
    assert response.json()['prix'] == 0.9

def test_delete_product_api():
    created = client.post('/products', json={
        'nom': 'Gomme', 'description': 'Gomme blanche', 'prix': 0.3, 'quantite_stock': 150
    }).json()
    product_id = created['id']
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 204

def test_delete_product_not_found_api():
    response = client.delete('/products/999')
    assert response.status_code == 404
