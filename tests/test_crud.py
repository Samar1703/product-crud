import pytest
from app import crud
from app.models import ProductCreate, ProductUpdate

@pytest.fixture(autouse=True)
def reset():
    crud.reset_store()

def test_create_product():
    data = ProductCreate(nom='Stylo', description='Stylo bleu', prix=1.5, quantite_stock=100)
    product = crud.create_product(data)
    assert product.id == 1
    assert product.nom == 'Stylo'
    assert product.prix == 1.5

def test_get_product():
    data = ProductCreate(nom='Cahier', description='Cahier A4', prix=3.0, quantite_stock=50)
    created = crud.create_product(data)
    found = crud.get_product(created.id)
    assert found is not None
    assert found.nom == 'Cahier'

def test_get_product_not_found():
    result = crud.get_product(999)
    assert result is None

def test_get_all_products():
    crud.create_product(ProductCreate(nom='P1', description='desc1', prix=1.0, quantite_stock=10))
    crud.create_product(ProductCreate(nom='P2', description='desc2', prix=2.0, quantite_stock=20))
    products = crud.get_all_products()
    assert len(products) == 2

def test_update_product():
    data = ProductCreate(nom='Crayon', description='Crayon HB', prix=0.5, quantite_stock=200)
    created = crud.create_product(data)
    updated = crud.update_product(created.id, ProductUpdate(prix=0.8))
    assert updated.prix == 0.8
    assert updated.nom == 'Crayon'

def test_update_product_not_found():
    result = crud.update_product(999, ProductUpdate(prix=1.0))
    assert result is None

def test_delete_product():
    data = ProductCreate(nom='Gomme', description='Gomme blanche', prix=0.3, quantite_stock=150)
    created = crud.create_product(data)
    success = crud.delete_product(created.id)
    assert success is True
    assert crud.get_product(created.id) is None

def test_delete_product_not_found():
    result = crud.delete_product(999)
    assert result is False
