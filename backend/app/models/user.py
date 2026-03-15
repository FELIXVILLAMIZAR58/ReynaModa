from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Address(BaseModel):
    id: Optional[str] = None
    city: str
    state: str
    street: str
    zipCode: str
    isDefault: bool = False

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    name: str
    phone: str
    avatar: Optional[str] = None
    role: str = "customer"  # "customer", "admin"
    addresses: List[Address] = []
    favorites: List[str] = []
    orders: List[str] = []
    createdAt: Optional[datetime] = None
    lastLogin: Optional[datetime] = None
    isActive: bool = True
    hashed_password: Optional[str] = None

class UserRegister(BaseModel):
    email: EmailStr
    name: str
    phone: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    addresses: Optional[List[Address]] = None
