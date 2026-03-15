"""
🏪 REYNA MODA - API v2.0
Tienda Online Premium con IA Marketing Automático
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Importar rutas
from app.routes import auth, products, orders, shipping, analytics, ai_marketing, chatbot, social_media
from app.database import get_db, db
from app.config import ALLOWED_ORIGINS, ENVIRONMENT

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear app FastAPI
app = FastAPI(
    title="REYNA MODA API",
    description="🏪 Tienda Online Premium con Agente IA de Marketing",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ════════════════════════════════════════════════════════════════════════════
# RUTAS
# ════════════════════════════════════════════════════════════════════════════

# Incluir routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(shipping.router)
app.include_router(analytics.router)
app.include_router(ai_marketing.router)
app.include_router(chatbot.router)
app.include_router(social_media.router)

# ════════════════════════════════════════════════════════════════════════════
# RUTAS PÚBLICAS
# ════════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["info"])
async def root():
    """Información del API"""
    return {
        "name": "REYNA MODA API",
        "version": "2.0.0",
        "environment": ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat(),
        "documentation": "/api/docs",
        "database": "Firebase Firestore" if db else "Demo Mode",
        "features": {
            "tienda_online": "✅ Catálogo, carrito, favoritos, checkout",
            "panel_admin": "✅ Gestión de productos, órdenes, usuarios",
            "ai_marketing": "✅ Mejora de imágenes, generación de videos, copywriting",
            "redes_sociales": "✅ Instagram, TikTok, publicaciones automáticas",
            "chatbot": "✅ Asistente de ventas inteligente",
            "pagos": "✅ Nequi, transferencia, contra entrega",
            "envios": "✅ Cálculo automático, envío local y nacional"
        }
    }

@app.get("/api/health", tags=["health"])
async def health_check():
    """Health check del API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if db else "demo_mode",
        "environment": ENVIRONMENT
    }

@app.get("/api/info", tags=["info"])
async def api_info():
    """Información del API"""
    return {
        "name": "REYNA MODA - Tienda Online Premium",
        "version": "2.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "products": "/api/products",
            "orders": "/api/orders",
            "shipping": "/api/shipping",
            "analytics": "/api/analytics",
            "ai": "/api/ai",
            "chat": "/api/chat",
            "social": "/api/social"
        }
    }

# ════════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ════════════════════════════════════════════════════════════════════════════

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# ════════════════════════════════════════════════════════════════════════════
# STARTUP & SHUTDOWN
# ════════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """Evento de inicio"""
    logger.info("🚀 REYNA MODA API iniciando...")
    logger.info(f"📊 Ambiente: {ENVIRONMENT}")
    logger.info(f"🔌 Base de datos: {'Firestore' if db else 'Demo Mode'}")
    logger.info("✅ API lista para recibir solicitudes")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de shutdown"""
    logger.info("🛑 REYNA MODA API cerrando...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=ENVIRONMENT == "development",
        log_level="info"
    )
