from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from app.services.ai_marketing_service import AIMarketingService
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["ai-marketing"])

@router.post("/enhance-image")
async def enhance_image(
    image_url: str = None,
    file: UploadFile = File(None)
):
    """Mejorar imagen del producto"""
    try:
        image_data = None
        if file:
            image_data = await file.read()
        
        result = await AIMarketingService.enhance_image(image_url, image_data)
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error mejorando imagen: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-copy")
async def generate_copy(
    product_name: str,
    category: str,
    description: str
):
    """Generar texto de marketing"""
    try:
        result = await AIMarketingService.generate_promotional_copy(
            product_name, category, description
        )
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error generando copy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-video-script")
async def generate_video_script(
    product_name: str,
    description: str,
    category: str
):
    """Generar script para video promocional"""
    try:
        result = await AIMarketingService.generate_video_script(
            product_name, description, category
        )
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error generando script: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-seo")
async def generate_seo(
    product_name: str,
    category: str,
    description: str
):
    """Generar contenido SEO"""
    try:
        result = await AIMarketingService.generate_seo_content(
            product_name, category, description
        )
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error generando SEO: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-publish")
async def auto_publish(
    product_id: str,
    product_name: str,
    category: str,
    description: str,
    image_url: str,
    db = Depends(get_db)
):
    """Publicar automáticamente en redes sociales"""
    try:
        if not db:
            raise HTTPException(status_code=500, detail="Database not available")
        
        # Generar copy
        copy_result = await AIMarketingService.generate_promotional_copy(
            product_name, category, description
        )
        
        copy = copy_result.get("copies", {}).get("instagram", "")
        
        # Publicar en Instagram
        result = await AIMarketingService.auto_publish_to_instagram(
            db, product_id, {
                "name": product_name,
                "category": category,
                "description": description
            }, copy, image_url
        )
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error publicando automáticamente: {e}")
        raise HTTPException(status_code=500, detail=str(e))
