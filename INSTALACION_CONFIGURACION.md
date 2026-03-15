# 🚀 GUÍA DE INSTALACIÓN Y CONFIGURACIÓN

## 📋 Requisitos

- Python 3.9+
- Node.js 16+
- Firebase (Firestore)
- Cuentas de redes sociales (Instagram, TikTok)

---

## 🔧 INSTALACIÓN DEL BACKEND

### 1. Crear Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
```

### 4. Iniciar el servidor

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El API estará disponible en: http://localhost:8000

---

## 📊 CONFIGURACIÓN DE FIREBASE

### 1. Crear proyecto en Firebase

1. Ir a https://firebase.google.com
2. Click en "Go to console"
3. Click en "Add project"
4. Rellenar datos del proyecto

### 2. Habilitaredes Firestore

1. En el dashboard, ir a "Build" → "Firestore Database"
2. Click en "Create Database"
3. Seleccionar región más cercana
4. Iniciar en modo test (solo para desarrollo)

### 3. Generar credenciales

1. Ir a "Project Settings" → "Service Accounts"
2. Click en "Generate new private key"
3. Copiar el contenido JSON
4. Pegar en `.env` como `FIREBASE_PRIVATE_KEY`

### 4. Crear colecciones en Firestore

```javascript
// Estructura inicial
collections: [
  "users",
  "products",
  "orders",
  "inventory",
  "analytics",
  "marketing_content",
  "social_posts"
]
```

---

## 🎨 INSTALACIÓN DEL FRONTEND

### 1. Crear proyecto React

```bash
cd frontend
npm install
```

### 2. Configurar variables de entorno

```bash
# Crear archivo .env
VITE_API_URL=http://localhost:8000/api
```

### 3. Iniciar servidor de desarrollo

```bash
npm run dev
```

Frontend disponible en: http://localhost:5173

---

## 🔑 CONFIGURACIÓN DE REDES SOCIALES

### 📸 Instagram (Meta Graph API)

1. Ir a https://developers.facebook.com
2. Create App → Business
3. Agregar producto: Instagram Graph API
4. Obtener Access Token
5. Copiar en `.env`:
   ```
   IG_ACCESS_TOKEN=tu_token
   IG_BUSINESS_ID=tu_business_id
   ```

### 🎵 TikTok

1. Ir a https://developers.tiktok.com
2. Create app
3. Agregar "TikTok Web API"
4. Obtener credenciales
5. Copiar en `.env`:
   ```
   TIKTOK_CLIENT_ID=tu_id
   TIKTOK_CLIENT_SECRET=tu_secret
   TIKTOK_ACCESS_TOKEN=tu_token
   ```

### 💬 WhatsApp (Meta)

1. Usar mismo Business App de Facebook
2. Agregar producto: WhatsApp Business Platform
3. Obtener Access Token
4. Copiar en `.env`:
   ```
   WA_ACCESS_TOKEN=tu_token
   WA_PHONE_ID=tu_phone_id
   ```

---

## 🤖 CONFIGURACIÓN DE IA

### OpenAI GPT-4

1. Ir a https://platform.openai.com
2. Create API key
3. Copiar en `.env`:
   ```
   OPENAI_API_KEY=tu_api_key
   ```

### Stability AI (Generación de imágenes)

1. Ir a https://platform.stabilityai.com
2. Create account
3. Obtener API key
4. Copiar en `.env`:
   ```
   STABILITY_API_KEY=tu_api_key
   ```

---

## 💳 CONFIGURACIÓN DE PAGOS

### Nequi

1. Ir a https://www.nequi.com/negocio
2. Solicitar API access
3. Obtener API key
4. Copiar en `.env`:
   ```
   NEQUI_API_KEY=tu_api_key
   ```

---

## 📝 DATOS DE PRUEBA

### Crear usuario administrador

```bash
# A través del endpoint POST /api/auth/register
POST http://localhost:8000/api/auth/register
{
  "email": "admin@reynamoda.com",
  "name": "Administrador",
  "phone": "573001234567",
  "password": "Admin@2025"
}
```

### Crear productos de prueba

```bash
POST http://localhost:8000/api/products
Authorization: Bearer {token}
{
  "name": "Vestido Negro Elegante",
  "description": "Vestido negro de gala premium",
  "price": 89.99,
  "salePrice": 69.99,
  "category": "vestidos",
  "sizes": ["XS", "S", "M", "L", "XL"],
  "colors": ["negro"],
  "stock": 25,
  "tags": ["nuevo", "oferta"]
}
```

---

## ✅ VERIFICACIÓN

### Probar endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Info del API
curl http://localhost:8000/api/info

# Listar productos
curl http://localhost:8000/api/products

# Calcular envío
curl -X POST http://localhost:8000/api/shipping/calculate?city=Bucaramanga&weight_kg=1

# Chat
curl -X POST http://localhost:8000/api/chat/message -d "hola" -H "Content-Type: application/json"
```

---

## 🐳 DOCKER (Opcional)

### Build

```bash
docker build -t reyna-moda-api .
```

### Run

```bash
docker run -p 8000:8000 --env-file .env reyna-moda-api
```

---

## 📦 DEPLOYMENT

### Heroku

```bash
heroku create reyna-moda-api
git push heroku main
```

### Railway.app

1. Conectar repo de GitHub
2. Agregar variables de entorno
3. Deploy automático

### Google Cloud Run

```bash
gcloud run deploy reyna-moda-api \
  --source . \
  --region us-central1 \
  --set-env-vars-from .env
```

---

## 🆘 TROUBLESHOOTING

### "Firebase credentials not found"

- Verificar que `.env` tiene `FIREBASE_PRIVATE_KEY` correcto
- Si no tienes Firebase, el API funcionará en modo demo

### "Module not found: fastapi"

```bash
pip install fastapi uvicorn
```

### Puerto 8000 ya en uso

```bash
# Cambiar puerto
python -m uvicorn app.main:app --port 8001
```

### CORS Error

- Verificar `ALLOWED_ORIGINS` en `.env`
- Debe incluir `http://localhost:3000` y `http://localhost:5173`

---

## 📞 SOPORTE

Para más información:
- 📧 support@reynamoda.com
- 🔗 docs.reynamoda.com
- 💬 Discord: community.reynamoda.com
