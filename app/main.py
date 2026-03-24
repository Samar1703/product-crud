from fastapi import FastAPI, HTTPException
from app.models import ProductCreate, ProductUpdate
from app import crud

app = FastAPI(title='Product CRUD API')

@app.get('/products')
def list_products():
    return crud.get_all_products()

@app.get('/products/{product_id}')
def read_product(product_id: int):
    product = crud.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Produit non trouvé')
    return product

@app.post('/products', status_code=201)
def create_product(data: ProductCreate):
    return crud.create_product(data)

@app.put('/products/{product_id}')
def update_product(product_id: int, data: ProductUpdate):
    product = crud.update_product(product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail='Produit non trouvé')
    return product

@app.delete('/products/{product_id}', status_code=204)
def delete_product(product_id: int):
    success = crud.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail='Produit non trouvé')
