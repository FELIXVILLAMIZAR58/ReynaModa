from fastapi import APIRouter, Depends
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard_analytics():
    """Obtener analítica del dashboard"""
    return {
        "visits": 1250,
        "uniqueVisitors": 850,
        "pageViews": 3400,
        "ordersCreated": 25,
        "totalRevenue": 1875.50,
        "avgOrderValue": 75.02,
        "conversionRate": 2.94,
        "cartAbandonmentRate": 45.2
    }

@router.get("/products-bestsellers")
async def get_bestseller_products():
    """Obtener productos más vendidos"""
    return {
        "period": "last_30_days",
        "products": [
            {"id": "prod_001", "name": "Vestido Negro", "sales": 15},
            {"id": "prod_002", "name": "Blusa Dorada", "sales": 12},
            {"id": "prod_003", "name": "Pantalón Blanco", "sales": 10}
        ]
    }

@router.get("/revenue")
async def get_revenue_analytics(period: str = "monthly"):
    """Obtener datos de ingresos"""
    return {
        "period": period,
        "revenue": 15420.50,
        "orders": 154,
        "avgOrderValue": 100.13
    }
