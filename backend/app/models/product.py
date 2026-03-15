from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SEO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = []

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: float
    salePrice: Optional[float] = None
    category: str
    sizes: List[str] = []
    colors: List[str] = []
    stock: int
    images: List[str] = []
    video: Optional[str] = None
    tags: List[str] = []
    seo: Optional[SEO] = None
    rating: Optional[float] = 0.0
    reviews: Optional[int] = 0
    active: bool = True
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    salePrice: Optional[float] = None
    category: str
    sizes: List[str]
    colors: List[str]
    stock: int
    tags: List[str] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    salePrice: Optional[float] = None
    stock: Optional[int] = None
    active: Optional[bool] = None
    tags: Optional[List[str]] = None
