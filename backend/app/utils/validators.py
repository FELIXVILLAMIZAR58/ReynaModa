import re
from typing import Optional

def validate_email(email: str) -> bool:
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validar formato de teléfono colombiano"""
    pattern = r'^(?:\+57|0)?3[0-9]{9}$'
    return bool(re.match(pattern, phone))

def validate_password(password: str) -> bool:
    """Validar fortaleza de contraseña"""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def validate_zipcode(zipcode: str) -> bool:
    """Validar código postal colombiano"""
    return len(zipcode) >= 5

def validate_price(price: float, sale_price: Optional[float] = None) -> bool:
    """Validar precios"""
    if price <= 0:
        return False
    if sale_price and (sale_price <= 0 or sale_price >= price):
        return False
    return True
