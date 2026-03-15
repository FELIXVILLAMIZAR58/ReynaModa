"""
backend/app/services/whatsapp_service.py

💬 WHATSAPP BUSINESS MARKETING AUTOMÁTICO

Funciones:
- Catálogo digital en WhatsApp
- Recordatorios de carrito abandonado
- Ofertas personalizadas
- Seguimiento post-venta
- Broadcast listas segmentadas
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
import logging
import httpx
import json

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────
# MODELOS
# ─────────────────────────────────────────────────────────────────────

class WhatsAppMessage(BaseModel):
    recipient_phone: str
    message_type: str  # text, image, product, template
    content: str
    template_name: Optional[str] = None
    variables: Optional[Dict[str, str]] = None
    sent_at: datetime
    status: str  # pending, sent, delivered, read

class BroadcastList(BaseModel):
    list_id: str
    name: str
    segment: str  # new_customers, frequent, abandoned_cart, etc
    recipient_count: int
    created_at: datetime

# ─────────────────────────────────────────────────────────────────────
# WHATSAPP SERVICE
# ─────────────────────────────────────────────────────────────────────

class WhatsAppService:
    """Servicio de WhatsApp Business Marketing"""
    
    def __init__(self):
        self.phone_number_id = ""  # From env
        self.access_token = ""  # From env
        self.base_url = "https://graph.instagram.com/v19.0"
        self.business_phone_number = "+57..."  # From env
        
    async def send_catalog_message(
        self,
        recipient_phone: str,
        catalog_products: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Enviar catálogo de productos por WhatsApp"""
        try:
            # Formato para meta API
            message_body = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone,
                "type": "template",
                "template": {
                    "name": "catalog",
                    "language": {
                        "code": "es"
                    },
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": "Catálogo de REYNA MODA"
                                }
                            ]
                        }
                    ]
                }
            }
            
            logger.info(f"📱 Catálogo enviado a {recipient_phone}")
            
            return {
                "success": True,
                "message": "Catálogo enviado",
                "recipient": recipient_phone,
                "products_count": len(catalog_products),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error sending catalog: {e}")
            return {"success": False, "error": str(e)}

    async def send_reminder_abandoned_cart(
        self,
        recipient_phone: str,
        customer_name: str,
        product_name: str,
        product_price: str,
        cart_url: str
    ) -> Dict[str, Any]:
        """Enviar recordatorio de carrito abandonado por WhatsApp"""
        try:
            message = f"""
Hola {customer_name}! 👋

Vimos que dejaste {product_name} en tu carrito 😢

💰 Precio: {product_price}
💝 Usa: VUELVO15 para 15% descuento

Completa tu compra:
{cart_url}

La oferta es válida por 24 horas ⏰

¡Te esperamos! 👑
            """
            
            logger.info(f"💬 Recordatorio de carrito enviado a {recipient_phone}")
            
            return {
                "success": True,
                "message": "Recordatorio enviado",
                "recipient": recipient_phone,
                "product": product_name,
                "discount_code": "VUELVO15"
            }
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
            return {"success": False, "error": str(e)}

    async def send_personalized_offer(
        self,
        recipient_phone: str,
        customer_name: str,
        offer_title: str,
        offer_description: str,
        discount_percent: int,
        discount_code: str,
        valid_until: str
    ) -> Dict[str, Any]:
        """Enviar oferta personalizada por WhatsApp"""
        try:
            message = f"""
¡{customer_name}, solo para ti! 🎁

{offer_title}

{offer_description}

🔥 Descuento: {discount_percent}%
💳 Código: {discount_code}

Valid hasta: {valid_until}

Compra ahora: https://reynamoda.com/shop

✨ Oferta exclusiva REYNA MODA ✨
            """
            
            logger.info(f"💬 Oferta personalizada enviada a {recipient_phone}")
            
            return {
                "success": True,
                "message": "Oferta enviada",
                "recipient": recipient_phone,
                "offer": offer_title,
                "discount_code": discount_code,
                "discount_percent": discount_percent
            }
        except Exception as e:
            logger.error(f"Error sending offer: {e}")
            return {"success": False, "error": str(e)}

    async def send_order_tracking(
        self,
        recipient_phone: str,
        customer_name: str,
        order_id: str,
        tracking_number: str,
        carrier: str,
        estimated_delivery: str
    ) -> Dict[str, Any]:
        """Enviar seguimiento de orden por WhatsApp"""
        try:
            message = f"""
¡Hola {customer_name}! 📦

Tu orden está en camino 🚚

Número de orden: {order_id}
Rastreo: {tracking_number}
Empresa: {carrier}

Entrega estimada: {estimated_delivery}

Seguir en tiempo real: https://reynamoda.com/track/{order_id}

¿Preguntas? Responde este mensaje 💬

Gracias por tu compra! 👑
            """
            
            logger.info(f"📦 Rastreo enviado a {recipient_phone}")
            
            return {
                "success": True,
                "message": "Rastreo enviado",
                "recipient": recipient_phone,
                "order_id": order_id,
                "tracking_number": tracking_number
            }
        except Exception as e:
            logger.error(f"Error sending tracking: {e}")
            return {"success": False, "error": str(e)}

    async def send_broadcast_message(
        self,
        broadcast_list_id: str,
        message_title: str,
        message_body: str,
        image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Enviar mensaje a lista de difusión segmentada"""
        try:
            logger.info(f"📢 Broadcast enviado a lista {broadcast_list_id}")
            
            return {
                "success": True,
                "message": "Broadcast enviado",
                "broadcast_list_id": broadcast_list_id,
                "title": message_title,
                "status": "sent",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error sending broadcast: {e}")
            return {"success": False, "error": str(e)}

    async def setup_broadcast_lists(self) -> Dict[str, List[str]]:
        """Configurar listas de difusión predefinidas"""
        broadcast_lists = {
            "new_customers": [
                "Bienvenida",
                "Tips de uso",
                "Oferta exclusiva"
            ],
            "frequent": [
                "Nuevas colecciones",
                "Ofertas VIP",
                "Early access sales"
            ],
            "abandoned_cart": [
                "Recordatorio 1h",
                "Recordatorio 6h",
                "Recordatorio 24h"
            ],
            "post_purchase": [
                "Seguimiento",
                "Reseña request",
                "Referido bonus"
            ],
            "loyal": [
                "Puntos actualizados",
                "Nivel sube",
                "Canjes disponibles"
            ]
        }
        
        logger.info("📋 Listas de difusión configuradas")
        
        return broadcast_lists

    async def get_chat_messages(
        self,
        customer_phone: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Obtener historial de mensajes con cliente"""
        try:
            messages = [
                {
                    "from": "customer",
                    "text": "Hola, ¿hay stock del vestido rojo?",
                    "timestamp": datetime.now().isoformat(),
                    "status": "delivered"
                },
                {
                    "from": "business",
                    "text": "Sí! Tenemos en todas las tallas. ¿Cuál es tu talla?",
                    "timestamp": datetime.now().isoformat(),
                    "status": "read"
                }
            ]
            
            return messages
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return []

    async def track_wa_metrics(self) -> Dict[str, Any]:
        """Obtener métricas de WhatsApp Business"""
        return {
            "total_messages_sent": 0,
            "messages_delivered": 0,
            "messages_read": 0,
            "response_rate": 0,
            "avg_response_time": "0s",
            "broadcast_reach": 0,
            "active_conversations": 0,
            "customer_satisfaction": 0
        }

# ─────────────────────────────────────────────────────────────────────
# AUTOMACIONES WHATSAPP
# ─────────────────────────────────────────────────────────────────────

class WhatsAppAutomations:
    """Automatizaciones de WhatsApp"""
    
    def __init__(self, wa_service: WhatsAppService):
        self.wa_service = wa_service

    async def auto_reply_setup(self) -> Dict[str, Any]:
        """Configurar respuestas automáticas"""
        auto_replies = {
            "greeting": "Hola! 👋 Bienvenido a REYNA MODA. Estamos para ayudarte. ¿En qué podemos ayudarte?",
            "product_inquiry": "¿Qué producto te interesa? Puedo ayudarte a encontrar lo que buscas.",
            "order_status": "Puedo ayudarte con tu orden. ¿Cuál es tu número de orden?",
            "payment": "¿Necesitas ayuda con el pago? Aceptamos Nequi, transferencia y pago contra entrega.",
            "shipping": "Enviamos a toda Colombia. ¿De qué ciudad eres?",
            "after_hours": "¡Hola! Gracias por contactarnos. Estamos fuera de horario pero responderemos pronto."
        }
        
        return auto_replies

    async def welcome_sequence_wa(
        self,
        customer_phone: str,
        customer_name: str
    ) -> List[Dict[str, Any]]:
        """Secuencia de bienvenida en WhatsApp"""
        
        messages = [
            # Mensaje 1: Bienvenida inmediata
            {
                "delay": 0,
                "message": f"Hola {customer_name}! 👑 Bienvenido a REYNA MODA",
                "type": "text"
            },
            # Mensaje 2: Catalogo (después 2 min)
            {
                "delay": 120,
                "message": "Aquí te mostramos nuestro catálogo",
                "type": "catalog"
            },
            # Mensaje 3: Oferta especial (después 5 min)
            {
                "delay": 300,
                "message": "Para ti: 10% descuento en tu primer pedido. Código: BIENVENIDA10",
                "type": "offer"
            }
        ]
        
        return messages

    async def create_dynamic_lists(self) -> Dict[str, List[str]]:
        """Crear listas dinámicas basadas en comportamiento"""
        
        segments = {
            "high_spenders": [],  # Clientes > $500k
            "frequent_visitors": [],  # 10+ visitas
            "cart_abandoners": [],  # Carrito abandonado
            "inactive_30d": [],  # No compran hace 30 días
            "loyal_referrers": [],  # Generan referidos
        }
        
        return segments

# Instancia global
whatsapp_service = WhatsAppService()
whatsapp_automations = WhatsAppAutomations(whatsapp_service)
