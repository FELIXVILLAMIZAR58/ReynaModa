from passlib.context import CryptContext
from app.utils.jwt_utils import create_access_token, verify_token
from app.models.user import User, UserLogin
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Servicio de autenticación"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Encriptar contraseña con bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_token(user_id: str, email: str, role: str = "customer") -> dict:
        """Crear token JWT"""
        token = create_access_token({
            "sub": user_id,
            "email": email,
            "role": role
        })
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verificar token JWT"""
        return verify_token(token)
    
    @staticmethod
    async def authenticate_user(db, email: str, password: str) -> dict:
        """Autenticar usuario"""
        try:
            # Buscar usuario por email
            users = db.collection("users").where("email", "==", email).stream()
            user_doc = None
            
            for doc in users:
                user_doc = doc
                break
            
            if not user_doc:
                return {"error": "Usuario no encontrado", "code": 401}
            
            user_data = user_doc.to_dict()
            
            # Verificar contraseña
            if not AuthService.verify_password(password, user_data.get("hashed_password", "")):
                return {"error": "Contraseña incorrecta", "code": 401}
            
            # Actualizar último login
            db.collection("users").document(user_doc.id).update({
                "lastLogin": datetime.now(timezone.utc)
            })
            
            # Generar token
            token_data = AuthService.create_token(
                user_doc.id,
                user_data["email"],
                user_data.get("role", "customer")
            )
            
            return {
                "token": token_data["access_token"],
                "user": {
                    "id": user_doc.id,
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "role": user_data.get("role")
                }
            }
        
        except Exception as e:
            logger.error(f"Error autenticando usuario: {e}")
            return {"error": "Error en autenticación", "code": 500}
    
    @staticmethod
    async def create_user(db, user_data: dict) -> dict:
        """Crear nuevo usuario"""
        try:
            # Verificar si el email ya existe
            existing = db.collection("users").where("email", "==", user_data["email"]).stream()
            for doc in existing:
                return {"error": "Email ya registrado", "code": 400}
            
            # Crear usuario
            user_doc = {
                "email": user_data["email"],
                "name": user_data["name"],
                "phone": user_data["phone"],
                "hashed_password": AuthService.hash_password(user_data["password"]),
                "role": "customer",
                "avatar": None,
                "addresses": [],
                "favorites": [],
                "orders": [],
                "createdAt": datetime.now(timezone.utc),
                "lastLogin": datetime.now(timezone.utc),
                "isActive": True
            }
            
            # Guardar en Firestore
            doc_ref = db.collection("users").document()
            doc_ref.set(user_doc)
            
            return {
                "id": doc_ref.id,
                "email": user_data["email"],
                "name": user_data["name"],
                "message": "Usuario registrado exitosamente"
            }
        
        except Exception as e:
            logger.error(f"Error creando usuario: {e}")
            return {"error": "Error registrando usuario", "code": 500}
