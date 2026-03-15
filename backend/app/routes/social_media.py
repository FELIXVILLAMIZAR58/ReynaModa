from fastapi import APIRouter, HTTPException, Depends
from app.services.social_media_service import SocialMediaService
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/social", tags=["social-media"])

@router.post("/instagram/publish")
async def publish_to_instagram(
    caption: str,
    image: str,
    hashtags: list = [],
    db = Depends(get_db)
):
    """Publicar en Instagram"""
    try:
        result = await SocialMediaService.publish_to_instagram(db, {
            "caption": caption,
            "image": image,
            "hashtags": hashtags
        })
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error publicando: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tiktok/publish")
async def publish_to_tiktok(
    title: str,
    video: str,
    description: str = "",
    hashtags: list = [],
    db = Depends(get_db)
):
    """Publicar en TikTok"""
    try:
        result = await SocialMediaService.publish_to_tiktok(db, {
            "title": title,
            "video": video,
            "description": description,
            "hashtags": hashtags
        })
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error publicando: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/instagram/feed")
async def get_instagram_feed(db = Depends(get_db)):
    """Obtener feed de Instagram"""
    try:
        result = await SocialMediaService.get_instagram_feed(db)
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error obteniendo feed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tiktok/videos")
async def get_tiktok_videos(db = Depends(get_db)):
    """Obtener videos de TikTok"""
    try:
        result = await SocialMediaService.get_tiktok_videos(db)
        
        if not result.get("success", True):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error obteniendo videos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
