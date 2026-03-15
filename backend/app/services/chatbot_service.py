import logging
from typing import List, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ChatbotService:
    """Servicio de Chatbot IA de Ventas"""
    
    PRODUCT_QUESTIONS = {
        "precio": "precio",
        "costo": "precio",
        "value": "precio",
        "talla": "size",
        "tallas": "sizes",
        "tamaño": "size",
        "color": "color",
        "colores": "colors",
        "disponible": "availability",
        "stock": "availability",
        "envio": "shipping",
        "envío": "shipping",
        "entrega": "shipping",
        "delivery": "shipping",
        "material": "material",
        "tela": "material",
        "oferta": "discount",
        "descuento": "discount",
        "promocion": "promotion"
    }
    
    @staticmethod
    def extract_intent(message: str) -> str:
        """Extraer intención del mensaje"""
        message_lower = message.lower()
        
        for keyword, intent in ChatbotService.PRODUCT_QUESTIONS.items():
            if keyword in message_lower:
                return intent
        
        return "general"
    
    @staticmethod
    async def get_response(message: str, db = None, product_id: str = None) -> dict:
        """Generar respuesta del chatbot"""
        try:
            intent = ChatbotService.extract_intent(message)
            
            responses = {
                "precio": {
                    "text": "Nuestros precios varían según el producto. ¿Hay algún producto específico que te interese? 😊",
                    "suggestions": ["Ver catálogo", "Filtrar por precio"]
                },
                "size": {
                    "text": "Tenemos tallas desde XS hasta XXL. ¿Qué talla necesitas?",
                    "suggestions": ["XS", "S", "M", "L", "XL", "XXL"]
                },
                "color": {
                    "text": "Disponemos de una amplia variedad de colores. ¿Cuál te atrae más?",
                    "suggestions": ["Negro", "Blanco", "Rojo", "Azul", "Rosa"]
                },
                "availability": {
                    "text": "¿Cuál producto te interesa? Te diré si está disponible. 📦",
                    "suggestions": ["Ver productos", "Catálogo"]
                },
                "shipping": {
                    "text": "🚚 En Bucaramanga y ciudades cercanas: envío local $5.000\nOtras ciudades: envío nacional desde $15.000\n\n¿A qué ciudad es?",
                    "suggestions": ["Bucaramanga", "Otra ciudad"]
                },
                "material": {
                    "text": "Usamos materiales premium: telas de calidad, cómodos y duraderos. ✨",
                    "suggestions": ["Ver productos", "Más información"]
                },
                "discount": {
                    "text": "¡Tenemos ofertas especiales! 🎉 Muchos productos con descuento. ¿Qué categoría te interesa?",
                    "suggestions": ["Vestidos", "Blusas", "Pantalones", "Accesorios"]
                },
                "promotion": {
                    "text": "Revisa nuestras promociones actuales. ¡Descuentos de hasta 30%! 💝",
                    "suggestions": ["Ver ofertas", "Comprar ahora"]
                },
                "general": {
                    "text": "Hola! 👋 Soy tu asistente de REYNA MODA. ¿En qué puedo ayudarte? Puedo:\n✓ Mostrar catálogo\n✓ Responder preguntas de productos\n✓ Ayudarte con el checkout\n✓ Resolver dudas de envío",
                    "suggestions": ["Catálogo", "Ofertas", "Envíos", "Contacto"]
                }
            }
            
            response = responses.get(intent, responses["general"])
            
            return {
                "success": True,
                "text": response["text"],
                "suggestions": response.get("suggestions", []),
                "intent": intent,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error en chatbot: {e}")
            return {
                "success": False,
                "text": "Disculpa, hubo un error. Por favor intenta de nuevo.",
                "error": str(e)
            }
    
    @staticmethod
    async def recommend_products(db, user_id: str = None, category: str = None) -> dict:
        """Recomendar productos"""
        try:
            recommendations = []
            
            if db:
                query = db.collection("products").where("active", "==", True)
                
                if category:
                    query = query.where("category", "==", category)
                
                docs = list(query.limit(5).stream())
                
                for doc in docs:
                    product = doc.to_dict()
                    product["id"] = doc.id
                    recommendations.append(product)
            
            return {
                "success": True,
                "recommendations": recommendations,
                "message": "Te mostramos nuestras recomendaciones"
            }
        
        except Exception as e:
            logger.error(f"Error recomendando productos: {e}")
            return {"success": False, "error": str(e)}
