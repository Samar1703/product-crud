from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: int
    nom: str
    description: str
    prix: float = Field(gt=0)
    quantite_stock: int = Field(ge=0)

class ProductCreate(BaseModel):
    nom: str
    description: str
    prix: float = Field(gt=0)
    quantite_stock: int = Field(ge=0)

class ProductUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    prix: Optional[float] = Field(default=None, gt=0)
    quantite_stock: Optional[int] = Field(default=None, ge=0)
