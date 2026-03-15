# 🔧 CONFIGURACIÓN - REYNA MODA

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# 📍 Rutas
ROOT_DIR = Path(__file__).parent.parent

# 🔑 Claves y tokens
JWT_SECRET = os.environ.get("JWT_SECRET_KEY", "reyna_moda_secret_2025_super_secure")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# 🗄️ Base de datos
FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID", "reyna-moda"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
}

# 💳 Pagos
NEQUI_API_KEY = os.environ.get("NEQUI_API_KEY", "")
NEQUI_API_URL = "https://api.nequi.com/payment"

# 📱 Redes sociales
IG_ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")
IG_BUSINESS_ID = os.environ.get("IG_BUSINESS_ID", "")

TIKTOK_CLIENT_ID = os.environ.get("TIKTOK_CLIENT_ID", "")
TIKTOK_CLIENT_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET", "")
TIKTOK_ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN", "")

WA_ACCESS_TOKEN = os.environ.get("WA_ACCESS_TOKEN", "")
WA_PHONE_ID = os.environ.get("WA_PHONE_ID", "")

# 🤖 IA
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY", "")
ELEVEN_LABS_API_KEY = os.environ.get("ELEVEN_LABS_API_KEY", "")

# 📧 Email
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL", "noreply@reynamoda.com")

# 🌍 Envío
ENVIOS_API_KEY = os.environ.get("ENVIOS_API_KEY", "")
ENVIOS_API_URL = "https://api.envios.com"

# ⚙️ Aplicación
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

# 💰 Ciudades de envío local
LOCAL_SHIPPING_CITIES = [
    "Bucaramanga",
    "Floridablanca",
    "Girón",
    "Piedecuesta"
]

LOCAL_SHIPPING_COST = 5.00
NATIONAL_SHIPPING_BASE = 15.00
