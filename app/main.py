from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.models import ProductCreate, ProductUpdate
from app import crud

app = FastAPI(title="Product CRUD API")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>Product CRUD API</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; background: #f5f5f5; }
                h1 { color: #333; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                a { display: block; margin: 10px 0; padding: 12px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; text-align: center; }
                a:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Product CRUD API</h1>
                <p>Bienvenue sur l API de gestion de produits</p>
                <a href="/docs">Documentation Swagger</a>
                <a href="/products">Liste des produits (JSON)</a>
                <a href="/redoc">Documentation ReDoc</a>
            </div>
        </body>
    </html>
    """

@app.get("/products")
def list_products():
    return crud.get_all_products()

@app.get("/products/{product_id}")
def read_product(product_id: int):
    product = crud.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouve")
    return product

@app.post("/products", status_code=201)
def create_product(data: ProductCreate):
    return crud.create_product(data)

@app.put("/products/{product_id}")
def update_product(product_id: int, data: ProductUpdate):
    product = crud.update_product(product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouve")
    return product

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    success = crud.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouve")