import firebase_admin
from firebase_admin import credentials, firestore, storage
from app.config import FIREBASE_CONFIG, ROOT_DIR
from pathlib import Path
import json

# Inicializar Firebase
try:
    # Si hay credenciales en el diccionario
    if FIREBASE_CONFIG.get("private_key"):
        cred = credentials.Certificate(FIREBASE_CONFIG)
    else:
        # Buscar archivo de credenciales
        cred_path = ROOT_DIR / "firebase-credentials.json"
        if cred_path.exists():
            cred = credentials.Certificate(str(cred_path))
        else:
            raise Exception("Firebase credentials not found")
    
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
except Exception as e:
    print(f"⚠️ Firebase initialization error: {e}")
    print("ℹ️ Sistema funcionará sin Firebase en modo demo")
    db = None

async def get_db():
    """Dependency injection para Firestore"""
    return db
