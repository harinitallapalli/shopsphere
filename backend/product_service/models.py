from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = ""
    category: Optional[str] = "Uncategorized"
    image_url: Optional[str] = ""
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 100
    discount: Optional[str] = "10% OFF"
    stock: Optional[int] = 20


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    discount: Optional[str] = None
    stock: Optional[int] = None
