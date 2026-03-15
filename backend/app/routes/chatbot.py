from fastapi import APIRouter, HTTPException, Depends, WebSocket
from app.services.chatbot_service import ChatbotService
from app.database import get_db
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chatbot"])

@router.post("/message")
async def send_message(
    message: str,
    product_id: str = None,
    db = Depends(get_db)
):
    """Enviar mensaje al chatbot"""
    try:
        result = await ChatbotService.get_response(message, db, product_id)
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error en chatbot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations")
async def get_recommendations(
    category: str = None,
    user_id: str = None,
    db = Depends(get_db)
):
    """Obtener recomendaciones de productos"""
    try:
        result = await ChatbotService.recommend_products(db, user_id, category)
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error en recomendaciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quick-answers")
async def get_quick_answers():
    """Obtener respuestas rápidas frecuentes"""
    return {
        "faqs": [
            {
                "question": "¿Cuál es el costo del envío?",
                "answer": "En Bucaramanga y ciudades cercanas: $5.000. Otras ciudades: desde $15.000."
            },
            {
                "question": "¿Cuáles son las tallas disponibles?",
                "answer": "Contamos con tallas XS, S, M, L, XL, XXL y numeradas (32-46)."
            },
            {
                "question": "¿Cómo es el proceso de compra?",
                "answer": "1. Elige tu producto\n2. Selecciona talla y color\n3. Agrega al carrito\n4. Completa checkout\n5. Realiza pago"
            },
            {
                "question": "¿Aceptan devoluciones?",
                "answer": "Sí, acepto devoluciones en 30 días con producto en buen estado."
            },
            {
                "question": "¿Tienen métodos de pago?",
                "answer": "Sí: Nequi, Transferencia bancaria y Pago contra entrega."
            }
        ]
    }
