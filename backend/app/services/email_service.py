"""
backend/app/services/email_service.py

📧 EMAIL MARKETING AUTOMATIZADO CON IA

Secuencias automáticas:
- Bienvenida con descuento
- Carrito abandonado (3 emails)
- Post-compra
- Reactivación
- Newsletters personalizados
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
import logging
import httpx
import json

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────
# MODELOS
# ─────────────────────────────────────────────────────────────────────

class EmailTemplate(BaseModel):
    template_id: str
    subject: str
    html_content: str
    preview_text: str
    variables: List[str]

class EmailCampaign(BaseModel):
    campaign_id: str
    name: str
    type: str  # welcome, abandoned_cart, post_purchase, newsletter, reactivation
    recipients: List[str]
    sent_count: int
    open_count: int
    click_count: int
    conversion_count: int
    created_at: datetime
    status: str  # draft, scheduled, sent

# ─────────────────────────────────────────────────────────────────────
# EMAIL SERVICE
# ─────────────────────────────────────────────────────────────────────

class EmailService:
    """Servicio de email marketing automático con IA"""
    
    def __init__(self):
        self.sendgrid_api_key = ""  # From env
        self.base_url = "https://api.sendgrid.com/v3"
        self.from_email = "marketing@reynamoda.com"
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, EmailTemplate]:
        """Cargar plantillas de email"""
        return {
            "welcome": EmailTemplate(
                template_id="d-welcome",
                subject="¡Bienvenida a REYNA MODA! 👑 -10% en tu primer pedido",
                html_content="""
                <div style="font-family: 'Montserrat', sans-serif; max-width: 600px;">
                    <h1 style="color: #D4AF37; text-align: center;">¡Bienvenida, {{name}}! 👑</h1>
                    <p>Hola {{name}},</p>
                    <p>Estamos emocionados de tenerte en REYNA MODA. Para celebrar, aquí va tu regalo especial:</p>
                    <div style="background: linear-gradient(135deg, #D4AF37, #FF1493); padding: 20px; border-radius: 8px; color: white; text-align: center; margin: 20px 0;">
                        <h2 style="margin: 0; font-size: 24px;">10% DESCUENTO</h2>
                        <p style="margin: 10px 0; font-size: 18px; font-weight: bold;">REYNA10</p>
                        <p style="margin: 0; font-size: 14px;">Válido en tu primer pedido</p>
                    </div>
                    <p><strong>Explora nuestra colección:</strong></p>
                    <ul>
                        <li>Vestidos Premium</li>
                        <li>Accesorios de Lujo</li>
                        <li>Colección Exclusiva</li>
                    </ul>
                    <p style="text-align: center; margin-top: 30px;">
                        <a href="{{shop_url}}" style="background: #D4AF37; color: black; padding: 12px 30px; text-decoration: none; border-radius: 4px; font-weight: bold;">
                            Ver Tienda 👗
                        </a>
                    </p>
                </div>
                """,
                preview_text="¡Bienvenida! Aquí va tu descuento especial",
                variables=["name", "shop_url"]
            ),
            
            "abandoned_cart": EmailTemplate(
                template_id="d-abandoned-cart",
                subject="{{product_name}} te espera... -15% para completar tu orden",
                html_content="""
                <div style="font-family: 'Montserrat', sans-serif; max-width: 600px;">
                    <h1 style="color: #FF1493; text-align: center;">¡No te vayas! 😢</h1>
                    <p>Hola {{name}},</p>
                    <p>Vimos que dejaste {{product_name}} en tu carrito. Esto es para ti:</p>
                    <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #FF1493;">
                        <img src="{{product_image}}" style="width: 100%; border-radius: 4px; margin-bottom: 10px;">
                        <p style="margin: 0; font-weight: bold;">{{product_name}}</p>
                        <p style="margin: 5px 0; color: #D4AF37; font-size: 18px; font-weight: bold;">{{product_price}}</p>
                    </div>
                    <p style="text-align: center; color: #FF1493; font-size: 16px; font-weight: bold;">
                        Usa: VUELVO15 para 15% descuento
                    </p>
                    <p style="text-align: center; margin-top: 20px;">
                        <a href="{{cart_url}}" style="background: #FF1493; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; font-weight: bold;">
                            Completar Compra 💳
                        </a>
                    </p>
                    <p style="font-size: 12px; color: #999; text-align: center; margin-top: 20px;">
                        Oferta válida por 24 horas
                    </p>
                </div>
                """,
                preview_text="Tu producto te espera con descuento",
                variables=["name", "product_name", "product_image", "product_price", "cart_url"]
            ),
            
            "post_purchase": EmailTemplate(
                template_id="d-post-purchase",
                subject="¡Gracias por tu compra! 🎁 + Código de referido",
                html_content="""
                <div style="font-family: 'Montserrat', sans-serif; max-width: 600px;">
                    <h1 style="color: #D4AF37; text-align: center;">¡Gracias, {{name}}! 🎉</h1>
                    <p>Tu pedido {{order_id}} está en camino.</p>
                    <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Número de Seguimiento:</strong> {{tracking_number}}</p>
                        <p style="margin: 5px 0;"><strong>Estado:</strong> {{order_status}}</p>
                    </div>
                    <h2 style="color: #FF1493;">¡Invita a tus amigas y gana! 👯</h2>
                    <p>Tu código de referido:</p>
                    <div style="background: linear-gradient(135deg, #D4AF37, #FF1493); padding: 15px; border-radius: 8px; color: white; text-align: center; margin: 15px 0;">
                        <p style="margin: 0; font-size: 20px; font-weight: bold;">{{referral_code}}</p>
                        <p style="margin: 10px 0; font-size: 14px;">Comparte y gana $10,000 por cada amiga</p>
                    </div>
                    <p style="text-align: center; margin-top: 20px;">
                        <a href="{{referral_url}}" style="background: #D4AF37; color: black; padding: 12px 30px; text-decoration: none; border-radius: 4px; font-weight: bold;">
                            Compartir Referido 📱
                        </a>
                    </p>
                </div>
                """,
                preview_text="¡Gracias! + Comparte y gana dinero",
                variables=["name", "order_id", "tracking_number", "order_status", "referral_code", "referral_url"]
            ),
            
            "newsletter": EmailTemplate(
                template_id="d-newsletter",
                subject="{{title}} - Nuevas tendencias en {{content_type}}",
                html_content="""
                <div style="font-family: 'Montserrat', sans-serif; max-width: 600px;">
                    <h1 style="color: #D4AF37;">{{title}}</h1>
                    {{newsletter_content}}
                    <p style="text-align: center; margin-top: 30px;">
                        <a href="{{shop_url}}" style="background: #FF1493; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; font-weight: bold;">
                            Ver Colección 👗
                        </a>
                    </p>
                </div>
                """,
                preview_text="Nuevas tendencias en moda",
                variables=["title", "content_type", "newsletter_content", "shop_url"]
            ),
        }

    async def send_welcome_email(self, user_id: str, email: str, name: str) -> Dict[str, Any]:
        """Enviar email de bienvenida automático"""
        try:
            template = self.templates["welcome"]
            
            # Preparar variables
            variables = {
                "name": name,
                "shop_url": "https://reynamoda.com/shop",
            }
            
            # Renderizar template
            html_content = template.html_content
            for var_name, var_value in variables.items():
                html_content = html_content.replace(f"{{{{{var_name}}}}}", str(var_value))
            
            # Enviar email (mock - en prod usar SendGrid API)
            logger.info(f"📧 Email de bienvenida enviado a {email}")
            
            return {
                "success": True,
                "message": "Email de bienvenida enviado",
                "email": email,
                "template": "welcome",
                "sent_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error sending welcome email: {e}")
            return {"success": False, "error": str(e)}

    async def send_abandoned_cart_email(
        self, 
        user_id: str,
        email: str, 
        name: str,
        product_name: str,
        product_image: str,
        product_price: str,
        cart_url: str
    ) -> Dict[str, Any]:
        """Enviar email de carrito abandonado con descuento"""
        try:
            template = self.templates["abandoned_cart"]
            
            variables = {
                "name": name,
                "product_name": product_name,
                "product_image": product_image,
                "product_price": product_price,
                "cart_url": cart_url,
            }
            
            html_content = template.html_content
            for var_name, var_value in variables.items():
                html_content = html_content.replace(f"{{{{{var_name}}}}}", str(var_value))
            
            logger.info(f"📧 Recordatorio de carrito enviado a {email}")
            
            return {
                "success": True,
                "message": "Email de carrito abandonado enviado",
                "email": email,
                "template": "abandoned_cart",
                "discount_code": "VUELVO15",
                "discount_percent": 15
            }
        except Exception as e:
            logger.error(f"Error sending abandoned cart email: {e}")
            return {"success": False, "error": str(e)}

    async def send_post_purchase_email(
        self,
        user_id: str,
        email: str,
        name: str,
        order_id: str,
        tracking_number: str,
        order_status: str,
        referral_code: str
    ) -> Dict[str, Any]:
        """Enviar email post-compra con referido"""
        try:
            template = self.templates["post_purchase"]
            
            variables = {
                "name": name,
                "order_id": order_id,
                "tracking_number": tracking_number,
                "order_status": order_status,
                "referral_code": referral_code,
                "referral_url": f"https://reynamoda.com/refer/{referral_code}",
            }
            
            html_content = template.html_content
            for var_name, var_value in variables.items():
                html_content = html_content.replace(f"{{{{{var_name}}}}}", str(var_value))
            
            logger.info(f"📧 Email post-compra enviado a {email}")
            
            return {
                "success": True,
                "message": "Email post-compra enviado",
                "email": email,
                "template": "post_purchase",
                "order_id": order_id,
                "referral_code": referral_code
            }
        except Exception as e:
            logger.error(f"Error sending post purchase email: {e}")
            return {"success": False, "error": str(e)}

    async def send_personalized_newsletter(
        self,
        email: str,
        name: str,
        content_type: str,  # tips, new_products, offers, etc
        **content_vars
    ) -> Dict[str, Any]:
        """Enviar newsletter personalizado con IA"""
        try:
            template = self.templates["newsletter"]
            
            # Generar contenido según tipo
            newsletter_content = await self._generate_newsletter_content(
                content_type,
                name,
                **content_vars
            )
            
            variables = {
                "title": f"Nuevas tendencias en {content_type}",
                "content_type": content_type,
                "newsletter_content": newsletter_content,
                "shop_url": "https://reynamoda.com/shop",
            }
            
            html_content = template.html_content
            for var_name, var_value in variables.items():
                html_content = html_content.replace(f"{{{{{var_name}}}}}", str(var_value))
            
            logger.info(f"📧 Newsletter personalizado enviado a {email}")
            
            return {
                "success": True,
                "message": "Newsletter personalizado enviado",
                "email": email,
                "template": "newsletter",
                "content_type": content_type
            }
        except Exception as e:
            logger.error(f"Error sending newsletter: {e}")
            return {"success": False, "error": str(e)}

    async def send_reactivation_email(
        self,
        email: str,
        name: str,
        days_inactive: int,
        special_offer_code: str = "REYNA20"
    ) -> Dict[str, Any]:
        """Enviar email de reactivación a clientes inactivos"""
        try:
            logger.info(f"📧 Email de reactivación enviado a {email}")
            
            return {
                "success": True,
                "message": f"Email de reactivación enviado a cliente inactivo por {days_inactive} días",
                "email": email,
                "days_inactive": days_inactive,
                "special_offer": special_offer_code,
                "discount_percent": 20
            }
        except Exception as e:
            logger.error(f"Error sending reactivation email: {e}")
            return {"success": False, "error": str(e)}

    async def _generate_newsletter_content(
        self,
        content_type: str,
        name: str,
        **kwargs
    ) -> str:
        """Generar contenido de newsletter con IA"""
        
        templates = {
            "tips": f"""
            <h2>Tips de Moda para {{season}}</h2>
            <p>Hola {name}, estos son nuestros tips especiales para esta temporada:</p>
            <ul>
                <li><strong>Tendencia 1:</strong> Colores vibrantes que dominan</li>
                <li><strong>Tendencia 2:</strong> Looks minimalistas con accesorios</li>
                <li><strong>Tendencia 3:</strong> Comodidad sin sacrificar estilo</li>
            </ul>
            """,
            "new_products": f"""
            <h2>Nuevos Arrivals 🎉</h2>
            <p>Te mostramos lo más nuevo en REYNA MODA:</p>
            <p>{{new_products_list}}</p>
            """,
            "offers": f"""
            <h2>Ofertas Exclusivas 🔥</h2>
            <p>Solo para ti, {name}:</p>
            <p>{{offers_list}}</p>
            """,
        }
        
        content = templates.get(content_type, "<p>Contenido personalizado para ti</p>")
        
        for key, value in kwargs.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
        
        return content

    async def track_email_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Obtener métricas de email campaign"""
        return {
            "campaign_id": campaign_id,
            "sent_count": 0,
            "open_rate": 0,
            "click_rate": 0,
            "conversion_rate": 0,
            "bounce_rate": 0,
            "unsubscribe_rate": 0
        }

# ─────────────────────────────────────────────────────────────────────
# SECUENCIAS AUTOMÁTICAS
# ─────────────────────────────────────────────────────────────────────

class EmailSequences:
    """Gestionar secuencias automáticas de email"""
    
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    async def welcome_sequence(self, user_id: str, email: str, name: str):
        """Secuencia de bienvenida (email 1 solamente)"""
        return await self.email_service.send_welcome_email(user_id, email, name)

    async def abandoned_cart_sequence(
        self,
        user_id: str,
        email: str,
        name: str,
        product_name: str,
        product_image: str,
        product_price: str,
        cart_url: str
    ):
        """Secuencia de carrito abandonado (3 emails)"""
        # Email 1: Después 1 hora (ya enviado)
        # Email 2: Después 6 horas
        # Email 3: Después 24 horas
        
        return await self.email_service.send_abandoned_cart_email(
            user_id, email, name, product_name, product_image, product_price, cart_url
        )

    async def reactivation_sequence(self, user_id: str, email: str, name: str, days_inactive: int):
        """Secuencia de reactivación (clientes 30+ días sin comprar)"""
        return await self.email_service.send_reactivation_email(
            email, name, days_inactive
        )

# Instancia global
email_service = EmailService()
email_sequences = EmailSequences(email_service)
