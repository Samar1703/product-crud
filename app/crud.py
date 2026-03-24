from typing import Dict, Optional
from app.models import Product, ProductCreate, ProductUpdate

_products: Dict[int, Product] = {}
_next_id: int = 1

def get_all_products():
    return list(_products.values())

def get_product(product_id: int) -> Optional[Product]:
    return _products.get(product_id)

def create_product(data: ProductCreate) -> Product:
    global _next_id
    product = Product(id=_next_id, **data.model_dump())
    _products[_next_id] = product
    _next_id += 1
    return product

def update_product(product_id: int, data: ProductUpdate) -> Optional[Product]:
    product = _products.get(product_id)
    if not product:
        return None
    updated = product.model_dump()
    for key, value in data.model_dump(exclude_none=True).items():
        updated[key] = value
    _products[product_id] = Product(**updated)
    return _products[product_id]

def delete_product(product_id: int) -> bool:
    if product_id not in _products:
        return False
    del _products[product_id]
    return True

def reset_store():
    global _next_id
    _products.clear()
    _next_id = 1
