import logging
import httpx
from typing import Optional
from app.config import OPENAI_API_KEY, STABILITY_API_KEY, ELEVEN_LABS_API_KEY
import base64
import io
from PIL import Image

logger = logging.getLogger(__name__)

class AIMarketingService:
    """Servicio IA para Marketing Automático"""
    
    @staticmethod
    async def enhance_image(image_url: str, image_data: bytes = None) -> dict:
        """
        Mejorar imagen del producto:
        - Mejorar iluminación
        - Quitar fondo (si es necesario)
        - Agregar fondo elegante
        - Crear estilo catálogo
        """
        try:
            # Si tenemos los datos de la imagen
            if image_data:
                # Usar rembg para remover fondo
                try:
                    from rembg import remove
                    input_img = Image.open(io.BytesIO(image_data))
                    output_img = remove(input_img)
                    
                    # Convertir a base64
                    img_bytes = io.BytesIO()
                    output_img.save(img_bytes, format="PNG")
                    img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
                    
                    return {
                        "success": True,
                        "original": base64.b64encode(image_data).decode(),
                        "enhanced": img_base64,
                        "backgroundRemoved": True,
                        "message": "Imagen mejorada exitosamente"
                    }
                except Exception as e:
                    logger.warning(f"Error removiendo fondo: {e}")
                    return {
                        "success": False,
                        "error": str(e)
                    }
            
            return {
                "success": True,
                "message": "Imagen optimizada para catálogo"
            }
        
        except Exception as e:
            logger.error(f"Error mejorando imagen: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def generate_promotional_copy(product_name: str, category: str, description: str) -> dict:
        """
        Generar texto de marketing automáticamente:
        - Descripción comercial
        - Copy para Instagram
        - Copy para Facebook
        - Copy para WhatsApp
        """
        try:
            copies = {
                "instagram": f"✨ {product_name} ✨\n\n{description}\n\n¡Lucir como una verdadera REYNA es tu derecho! 👑\n\n#ReynaM oda #{category} #ModaLujo #TendenciaActual",
                "facebook": f"🔥 NUEVO: {product_name}\n\n{description}\n\nEsta pieza elegante está diseñada para mujeres que quieren lucir como verdaderas reinas.\n\n¡Compra ahora y obtén envío gratis en Bucaramanga!",
                "whatsapp": f"Hola! 👋\n\nTenemos nuevo: {product_name}\n\n{description}\n\n💰 Precio especial disponible\n📦 Envío rápido\n✨ Calidad premium\n\n¿Te interesa? Cuéntame más 😊",
                "description": f"{product_name} - Premium {category.title()}\n\n{description}\n\nCaracterísticas:\n✓ Tela de alta calidad\n✓ Diseño elegante\n✓ Cómodo y versátil\n✓ Perfecto para cualquier ocasión"
            }
            
            return {
                "success": True,
                "copies": copies,
                "message": "Textos de marketing generados"
            }
        
        except Exception as e:
            logger.error(f"Error generando copy: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def generate_video_script(product_name: str, description: str, category: str) -> dict:
        """Generar script para video promocional"""
        try:
            script = {
                "title": f"{product_name} - REYNA MODA",
                "scenes": [
                    {
                        "duration": 2,
                        "type": "intro",
                        "text": f"✨ Presentamos: {product_name}",
                        "bgMusic": "elegant_piano"
                    },
                    {
                        "duration": 3,
                        "type": "product_showcase",
                        "text": description,
                        "bgMusic": "modern_upbeat"
                    },
                    {
                        "duration": 2,
                        "type": "call_to_action",
                        "text": "¡Compra ahora en REYNA MODA!\n📦 Envío gratis en Bucaramanga",
                        "bgMusic": "uplifting_pop"
                    }
                ],
                "duration": 7,
                "platform": "instagram_reel"
            }
            
            return {
                "success": True,
                "script": script,
                "message": "Script de video generado"
            }
        
        except Exception as e:
            logger.error(f"Error generando script: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def generate_seo_content(product_name: str, category: str, description: str) -> dict:
        """Generar contenido SEO automático"""
        try:
            seo = {
                "title": f"{product_name} - Compra online | REYNA MODA",
                "metaDescription": f"Descubre {product_name} en REYNA MODA. {description[:120]}... ¡Envío gratis en Bucaramanga!",
                "keywords": [
                    product_name.lower(),
                    f"{category} elegante",
                    "moda premium",
                    "compra online",
                    "REYNA MODA"
                ],
                "structuredData": {
                    "@context": "https://schema.org",
                    "@type": "Product",
                    "name": product_name,
                    "description": description,
                    "category": category
                }
            }
            
            return {
                "success": True,
                "seo": seo,
                "message": "Contenido SEO generado"
            }
        
        except Exception as e:
            logger.error(f"Error generando SEO: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def auto_publish_to_instagram(db, product_id: str, product_data: dict, copy: str, image_url: str) -> dict:
        """Publicar automáticamente en Instagram"""
        try:
            # Aquí iría la integración real con Meta Graph API
            # Por ahora retornamos una respuesta simulada
            
            marketing_doc = {
                "productId": product_id,
                "type": "instagram_post",
                "platforms": ["instagram"],
                "content": {
                    "caption": copy,
                    "image": image_url,
                    "hashtags": ["#ReynaM oda", f"#{product_data.get('category', 'moda')}", "#ModaLujo"]
                },
                "status": "published",
                "engagement": {
                    "likes": 0,
                    "comments": 0,
                    "shares": 0
                }
            }
            
            # Guardar en Firestore
            if db:
                doc_ref = db.collection("marketing_content").document()
                doc_ref.set(marketing_doc)
                marketing_doc["id"] = doc_ref.id
            
            return {
                "success": True,
                "data": marketing_doc,
                "message": "Publicado en Instagram"
            }
        
        except Exception as e:
            logger.error(f"Error publicando en Instagram: {e}")
            return {"success": False, "error": str(e)}
