from fastapi import APIRouter, HTTPException, Depends, status
from app.models.user import UserRegister, UserLogin
from app.services.auth_service import AuthService
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
async def register(user_data: UserRegister, db = Depends(get_db)):
    """Registrar nuevo usuario"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await AuthService.create_user(db, user_data.dict())
    
    if not result.get("success", True) and "error" in result:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    
    return result

@router.post("/login")
async def login(credentials: UserLogin, db = Depends(get_db)):
    """Iniciar sesión"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not available")
    
    result = await AuthService.authenticate_user(db, credentials.email, credentials.password)
    
    if "error" in result:
        raise HTTPException(status_code=result.get("code", 401), detail=result["error"])
    
    return result

@router.post("/logout")
async def logout():
    """Cerrar sesión"""
    return {"message": "Session closed successfully"}

@router.get("/me")
async def get_current_user(token: str):
    """Obtener datos del usuario actual"""
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role")
    }
