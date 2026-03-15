from fastapi import APIRouter, HTTPException, Depends, Query
from app.services.shipping_service import ShippingService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/shipping", tags=["shipping"])

@router.post("/calculate")
async def calculate_shipping(city: str, weight_kg: float = 1.0):
    """Calcular costo de envío"""
    result = ShippingService.calculate_shipping(city, weight_kg)
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result

@router.get("/cities/local")
async def get_local_cities():
    """Obtener ciudades con envío local económico"""
    return {
        "cities": ShippingService.get_local_cities(),
        "local_cost": 5.00
    }

@router.get("/cities/all")
async def get_all_cities():
    """Obtener todas las ciudades principales"""
    return {
        "cities": ShippingService.get_all_cities()
    }
