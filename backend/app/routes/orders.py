from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.order import OrderCreate, OrderStatusUpdate
from app.services.order_service import OrderService
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("")
async def create_order(order: OrderCreate, user_id: str, db = Depends(get_db)):
    """Crear nueva orden"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await OrderService.create_order(db, user_id, order.dict())
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result

@router.get("")
async def get_user_orders(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db = Depends(get_db)
):
    """Obtener órdenes del usuario"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await OrderService.get_user_orders(db, user_id, skip, limit)
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result

@router.get("/admin/all")
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db = Depends(get_db)
):
    """Obtener todas las órdenes (admin)"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await OrderService.get_all_orders(db, skip, limit)
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result

@router.put("/{order_id}/status")
async def update_order_status(order_id: str, status_update: OrderStatusUpdate, db = Depends(get_db)):
    """Actualizar estado de orden (admin)"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await OrderService.update_order_status(
        db, order_id, status_update.status, status_update.notes
    )
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result
