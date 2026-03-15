from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.product import ProductCreate, ProductUpdate
from app.services.product_service import ProductService
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("")
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str = Query(None),
    min_price: float = Query(None, ge=0),
    max_price: float = Query(None, ge=0),
    search: str = Query(None),
    db = Depends(get_db)
):
    """Obtener todos los productos con filtros"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await ProductService.get_all_products(
        db, skip, limit, category, min_price, max_price, search
    )
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result

@router.get("/{product_id}")
async def get_product(product_id: str, db = Depends(get_db)):
    """Obtener un producto específico"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await ProductService.get_product(db, product_id)
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result

@router.post("")
async def create_product(product: ProductCreate, db = Depends(get_db)):
    """Crear nuevo producto (admin)"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await ProductService.create_product(db, product.dict())
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result

@router.put("/{product_id}")
async def update_product(product_id: str, product: ProductUpdate, db = Depends(get_db)):
    """Actualizar producto (admin)"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await ProductService.update_product(db, product_id, product.dict())
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result

@router.delete("/{product_id}")
async def delete_product(product_id: str, db = Depends(get_db)):
    """Eliminar producto (admin)"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await ProductService.delete_product(db, product_id)
    
    if not result.get("success", True):
        raise HTTPException(status_code=result.get("code", 500), detail=result.get("error"))
    
    return result
