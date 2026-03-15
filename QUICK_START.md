# ⚡ QUICK START - REYNA MODA v2.0

## 🚀 5 MINUTOS PARA EMPEZAR

### Paso 1: Instalar Backend (1 min)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Paso 2: Configurar .env (1 min)

```bash
cp .env.example .env

# Editar .env y agregar (mínimo):
JWT_SECRET_KEY=tu_secreto_aleatorio
ENVIRONMENT=development
DEBUG=true

# Firebase (opcional - funciona sin)
# FIREBASE_PROJECT_ID=...
# FIREBASE_PRIVATE_KEY=...
```

### Paso 3: Iniciar Servidor (30 seg)

```bash
python -m uvicorn app.main:app --reload
```

✅ **API disponible en**: `http://localhost:8000`

### Paso 4: Probar Endpoints (1 min)

```bash
# Health check
curl http://localhost:8000/api/health

# Ver documentación interactiva
# Ir a: http://localhost:8000/api/docs

# Crear producto
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vestido Prueba",
    "description": "Prueba",
    "price": 99.99,
    "category": "vestidos",
    "sizes": ["M"],
    "colors": ["negro"],
    "stock": 10,
    "tags": ["nuevo"]
  }'

# Ver productos
curl http://localhost:8000/api/products

# Chat con IA
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuál es el envío?"}'
```

### Paso 5: Verifi que todo funcione (1 min)

```bash
# Debe ver:
# ✅ Health check: {"status": "healthy"}
# ✅ Productos: {"success": true, "data": [...]}
# ✅ Chat: {"success": true, "text": "..."}
```

---

## 🎯 FUNCIONALIDADES CLAVE

### 🛍️ TIENDA
```
✅ Catálogo de productos
✅ Búsqueda y filtros
✅ Carrito (localStorage)
✅ Checkout (3 métodos de pago)
✅ Cálculo automático de envío
```

### 🤖 IA MARKETING
```
✅ Mejora de imágenes
✅ Generación de textos
✅ Generación de videos
✅ Publicación automática
✅ Analytics
```

### 💬 CHATBOT
```
✅ Responde preguntas
✅ Recomienda productos
✅ Info de envíos
✅ 24/7 disponible
```

### 📊 ADMIN
```
✅ Dashboard con KPIs
✅ CRUD de productos
✅ Gestión de órdenes
✅ Analítica completa
```

---

## 📚 DOCUMENTACIÓN

| Archivo | Propósito |
|---------|-----------|
| [README.md](README.md) | Resumen ejecutivo |
| [ARQUITECTURA_COMPLETA.md](ARQUITECTURA_COMPLETA.md) | Diseño técnico |
| [INSTALACION_CONFIGURACION.md](INSTALACION_CONFIGURACION.md) | Guía detallada |
| [PRUEBAS_ENDPOINTS.md](PRUEBAS_ENDPOINTS.md) | Test de APIs |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Lanzamiento a producción |
| [CARACTERISTICAS_PREMIUM.md](CARACTERISTICAS_PREMIUM.md) | Todas las features |
| [VERIFICACION_FUNCIONALIDADES.md](VERIFICACION_FUNCIONALIDADES.md) | Status de implementación |

---

## 🔥 EJEMPLOS RÁPIDOS

### Registrarse
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "name": "Juan",
    "phone": "573001234567",
    "password": "Pass123!"
  }'
```

### Iniciar sesión
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "Pass123!"
  }'
```

### Generar copy de marketing
```bash
curl -X POST http://localhost:8000/api/ai/generate-copy \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Vestido Negro Elegante",
    "category": "vestidos",
    "description": "Vestido elegante premium"
  }'
```

### Publicar en Instagram
```bash
curl -X POST http://localhost:8000/api/social/instagram/publish \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "✨ Nuevo vestido disponible",
    "image": "https://ejemplo.com/img.jpg",
    "hashtags": ["#ReynaM oda", "#Moda"]
  }'
```

### Chat AI
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son las tallas disponibles?"}'
```

---

## 🛠️ TROUBLESHOOTING

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Port 8000 in use"
```bash
# Cambiar puerto
python -m uvicorn app.main:app --port 8001
```

### Error: "Firebase credentials not found"
- El API funciona sin Firebase en modo demo
- Para usar Firestore, copiar credenciales a `.env`

### API no responde
```bash
# Verificar que está corriendo
curl http://localhost:8000/api/health

# Ver logs
# (Deben verse en la terminal donde corre uvicorn)
```

---

## 🧩 ESTRUCTURA

```
backend/
├── app/
│   ├── main.py           ← Inicia aquí
│   ├── config.py         ← Configuración
│   ├── database.py       ← Firebase
│   ├── routes/           ← 8 módulos API
│   ├── services/         ← Lógica
│   ├── models/           ← Datos
│   └── utils/            ← Funciones
├── requirements.txt      ← Dependencias
├── .env.example         ← Configurar
└── setup.py             ← Verificación
```

---

## 📈 NEXT STEPS

1. **Probar todos los endpoints** (15 min)
   - Usar Postman
   - Ver documentación en `/api/docs`

2. **Crear datos de prueba** (5 min)
   - Crear usuario
   - Crear productos
   - Crear órdenes

3. **Conectar Firebase** (10 min)
   - Crear proyecto en firebase.google.com
   - Descargar credenciales
   - Actualizar `.env`

4. **Configurar redes sociales** (15 min)
   - Instagram: developers.facebook.com
   - TikTok: developers.tiktok.com
   - Actualizar `.env`

5. **Frontend React** (próxima fase)
   - Instalar: `npm install`
   - Iniciar: `npm run dev`
   - Conectar API

---

## ✅ VERIFICACIÓN

```bash
# Ejecutar script de verificación
python setup.py

# Debe mostrar:
# ✅ Python 3.9+
# ✅ Virtual environment
# ✅ Dependencias instaladas
# ✅ Archivo .env
# ✅ Estructura de carpetas
```

---

## 🎮 JUEGA CON LA API

### Crear un ciclo completo

```bash
# 1. Registrarse
POST /api/auth/register

# 2. Iniciar sesión
POST /api/auth/login
# Guardar token

# 3. Crear producto
POST /api/products

# 4. Ver catálogo
GET /api/products

# 5. Calcular envío
POST /api/shipping/calculate

# 6. Crear orden
POST /api/orders

# 7. Ver mis órdenes
GET /api/orders

# 8. Ver admin orders
GET /api/admin/orders

# 9. Cambiar estado
PUT /api/orders/{id}/status

# 10. Ver analítica
GET /api/analytics/dashboard
```

---

## 🌟 LO MÁS DESTACADO

🤖 **AGENTE IA**
- Mejora imágenes automáticamente
- Genera videos promocionales
- Crea textos de marketing
- Publica en redes sociales

💬 **CHATBOT IA**
- Responde 24/7
- Inteligencia conversacional
- Recomendaciones personalizadas

📊 **ADMIN PANEL**
- Dashboard con KPIs
- Gestión completa de productos
- Seguimiento de órdenes
- Analítica detallada

---

## 🚀 LANZAR A PRODUCCIÓN

```bash
# 1. Heroku (10 min)
heroku create reyna-moda-api
git push heroku main

# 2. Railway.app (5 min)
# Conectar GitHub y deploy automático

# 3. Google Cloud Run (15 min)
gcloud run deploy reyna-moda-api --source .
```

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para más detalles.

---

## 💡 TIPS

- 📖 Lee la documentación en `/api/docs` (Swagger interactivo)
- 🧪 Prueba todos los endpoints antes de producción
- 🔒 Cambia JWT_SECRET_KEY en producción
- 📧 Configura SendGrid para emails
- 💳 Integra pasarelas de pago reales
- 📱 Usa Postman o Insomnia para testing
- 🔍 Revisa logs en tiempo real
- ⚡ Usa caché con Redis en producción

---

## 📞 AYUDA

- ❓ Preguntas → Lee INSTALACION_CONFIGURACION.md
- 🐛 Errores → Ver TROUBLESHOOTING
- 📡 Endpoints → PRUEBAS_ENDPOINTS.md
- 🚀 Deploy → DEPLOYMENT.md
- ✨ Features → CARACTERISTICAS_PREMIUM.md

---

## 🎉 ¡LISTO!

```
╔═══════════════════════════════════════╗
║  REYNA MODA v2.0 - ¡ACTIVO! 🚀        ║
║                                       ║
║  http://localhost:8000                ║
║  Docs: http://localhost:8000/api/docs ║
║                                       ║
║  ✅ 39 endpoints                      ║
║  ✅ Agente IA                         ║
║  ✅ Chatbot inteligente                ║
║  ✅ Redes sociales                    ║
║  ✅ Sistema de pagos                  ║
║                                       ║
║  Listos para lucir como una REYNA 👑 ║
╚═══════════════════════════════════════╝
```

---

**¡Que disfrutes! 🎀**
