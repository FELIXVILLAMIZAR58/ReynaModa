# 🧪 PRUEBAS DE ENDPOINTS - REYNA MODA API

## 🚀 Cómo ejecutar las pruebas

### Opción 1: Usando cURL

```bash
# Copiar y pegar en terminal
```

### Opción 2: Usando Postman

1. Importar `collection.json`
2. Configurar variables
3. Ejecutar suite de pruebas

### Opción 3: Usando Python

```python
import requests
BASE_URL = "http://localhost:8000/api"
```

---

## ✅ PRUEBAS DE ENDPOINTS

### 1️⃣ AUTENTICACIÓN

#### Registrarse
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Usuario Test",
    "phone": "573001234567",
    "password": "Test1234!"
  }'

# Respuesta esperada:
{
  "id": "user_001",
  "email": "test@example.com",
  "name": "Usuario Test",
  "message": "Usuario registrado exitosamente"
}
```

#### Iniciar sesión
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234!"
  }'

# Respuesta esperada:
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "user_001",
    "name": "Usuario Test",
    "email": "test@example.com",
    "role": "customer"
  }
}
```

---

### 2️⃣ PRODUCTOS

#### Obtener todos los productos
```bash
curl http://localhost:8000/api/products

# Con filtros:
curl "http://localhost:8000/api/products?category=vestidos&min_price=10&max_price=100"

# Con búsqueda:
curl "http://localhost:8000/api/products?search=negro"

# Con paginación:
curl "http://localhost:8000/api/products?skip=0&limit=20"
```

#### Obtener un producto
```bash
curl http://localhost:8000/api/products/prod_001
```

#### Crear producto (Admin)
```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vestido Negro Elegante",
    "description": "Vestido negro de gala, tela premium",
    "price": 89.99,
    "salePrice": 69.99,
    "category": "vestidos",
    "sizes": ["XS", "S", "M", "L", "XL"],
    "colors": ["negro", "rojo"],
    "stock": 25,
    "tags": ["nuevo", "oferta"]
  }'
```

#### Actualizar producto (Admin)
```bash
curl -X PUT http://localhost:8000/api/products/prod_001 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 79.99,
    "stock": 20
  }'
```

#### Eliminar producto (Admin)
```bash
curl -X DELETE http://localhost:8000/api/products/prod_001
```

---

### 3️⃣ ÓRDENES

#### Crear orden
```bash
curl -X POST http://localhost:8000/api/orders?user_id=user_001 \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "productId": "prod_001",
        "productName": "Vestido Negro",
        "price": 69.99,
        "quantity": 1,
        "size": "M",
        "color": "negro"
      }
    ],
    "shipping": {
      "address": "Calle 45 #23-45",
      "city": "Bucaramanga",
      "state": "Santander",
      "zipCode": "680001",
      "cost": 5.00,
      "estimatedDays": 2
    },
    "paymentMethod": "nequi",
    "notes": "Entregar después de las 5 PM"
  }'
```

#### Obtener mis órdenes
```bash
curl "http://localhost:8000/api/orders?user_id=user_001"
```

#### Obtener todas las órdenes (Admin)
```bash
curl http://localhost:8000/api/admin/orders
```

#### Actualizar estado de orden (Admin)
```bash
curl -X PUT http://localhost:8000/api/orders/order_001/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "notes": "Enviado por Servientrega"
  }'
```

---

### 4️⃣ ENVÍOS

#### Calcular envío
```bash
curl -X POST "http://localhost:8000/api/shipping/calculate?city=Bucaramanga&weight_kg=1"

# Respuesta:
{
  "success": true,
  "cost": 5.0,
  "estimatedDays": 2,
  "city": "Bucaramanga",
  "isLocal": true
}
```

#### Obtener ciudades con envío local
```bash
curl http://localhost:8000/api/shipping/cities/local
```

#### Obtener todas las ciudades
```bash
curl http://localhost:8000/api/shipping/cities/all
```

---

### 5️⃣ ANALÍTICA

#### Dashboard
```bash
curl http://localhost:8000/api/analytics/dashboard
```

#### Productos más vendidos
```bash
curl http://localhost:8000/api/analytics/products-bestsellers
```

#### Ingresos
```bash
curl http://localhost:8000/api/analytics/revenue?period=monthly
```

---

### 6️⃣ IA MARKETING

#### Mejorar imagen
```bash
curl -X POST http://localhost:8000/api/ai/enhance-image \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg"
  }'

# Respuesta:
{
  "success": true,
  "enhanced": "base64_image_data",
  "backgroundRemoved": true,
  "message": "Imagen mejorada exitosamente"
}
```

#### Generar textos de marketing
```bash
curl -X POST http://localhost:8000/api/ai/generate-copy \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Vestido Negro Elegante",
    "category": "vestidos",
    "description": "Vestido negro de gala premium"
  }'

# Respuesta:
{
  "success": true,
  "copies": {
    "instagram": "✨ Vestido Negro Elegante ✨...",
    "facebook": "🔥 NUEVO: Vestido Negro Elegante...",
    "whatsapp": "Hola! 👋 Tenemos nuevo: Vestido Negro...",
    "description": "Vestido Negro Elegante - Premium..."
  }
}
```

#### Generar script para video
```bash
curl -X POST http://localhost:8000/api/ai/generate-video-script \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Vestido Negro",
    "description": "Vestido elegante premium",
    "category": "vestidos"
  }'
```

#### Generar SEO
```bash
curl -X POST http://localhost:8000/api/ai/generate-seo \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Vestido Negro Elegante",
    "category": "vestidos",
    "description": "Vestido negro de gala premium"
  }'
```

#### Publicar automáticamente
```bash
curl -X POST http://localhost:8000/api/ai/auto-publish \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "prod_001",
    "product_name": "Vestido Negro",
    "category": "vestidos",
    "description": "Vestido elegante",
    "image_url": "https://example.com/image.jpg"
  }'
```

---

### 7️⃣ REDES SOCIALES

#### Publicar en Instagram
```bash
curl -X POST http://localhost:8000/api/social/instagram/publish \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "✨ Nuevo vestido disponible",
    "image": "https://example.com/image.jpg",
    "hashtags": ["#ReynaM oda", "#Moda"]
  }'
```

#### Publicar en TikTok
```bash
curl -X POST http://localhost:8000/api/social/tiktok/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nuevo Vestido Negro",
    "video": "https://example.com/video.mp4",
    "description": "Mira nuestro nuevo vestido",
    "hashtags": ["#ReynaM oda", "#Fashion"]
  }'
```

#### Obtener feed de Instagram
```bash
curl http://localhost:8000/api/social/instagram/feed
```

#### Obtener videos de TikTok
```bash
curl http://localhost:8000/api/social/tiktok/videos
```

---

### 8️⃣ CHATBOT

#### Enviar mensaje
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuál es el precio del envío?"
  }'

# Respuesta:
{
  "success": true,
  "text": "🚚 En Bucaramanga y ciudades cercanas: envío local $5.000...",
  "suggestions": ["Bucaramanga", "Otra ciudad"],
  "intent": "shipping",
  "timestamp": "2026-03-14T10:30:00Z"
}
```

#### Obtener recomendaciones
```bash
curl -X POST http://localhost:8000/api/chat/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "category": "vestidos"
  }'
```

#### Obtener respuestas frecuentes
```bash
curl http://localhost:8000/api/chat/quick-answers
```

---

### 9️⃣ INFORMACIÓN

#### Health Check
```bash
curl http://localhost:8000/api/health
```

#### Info del API
```bash
curl http://localhost:8000/api/info
```

---

## 📊 RESPUESTAS ESPERADAS

### Éxito (200)
```json
{
  "success": true,
  "data": {...},
  "message": "Operación completada"
}
```

### Error (400)
```json
{
  "detail": "Error en validación"
}
```

### No autorizado (401)
```json
{
  "detail": "Token inválido o expirado"
}
```

### No encontrado (404)
```json
{
  "detail": "Recurso no encontrado"
}
```

### Error servidor (500)
```json
{
  "detail": "Error interno del servidor"
}
```

---

## 🔄 FLUJO COMPLETO DE COMPRA

1. **Registrarse**
   ```bash
   POST /api/auth/register
   ```

2. **Iniciar sesión**
   ```bash
   POST /api/auth/login
   ```

3. **Obtener token** → Guardar en headers

4. **Ver productos**
   ```bash
   GET /api/products?category=vestidos
   ```

5. **Calcular envío**
   ```bash
   POST /api/shipping/calculate?city=Bucaramanga
   ```

6. **Crear orden**
   ```bash
   POST /api/orders
   ```

7. **Procesar pago**
   ```bash
   POST /api/payments/nequi
   ```

8. **Confirmar compra**
   ```bash
   GET /api/orders?user_id=xxx
   ```

---

## 📈 MONITOREO

```bash
# Ver logs en tiempo real
tail -f logs/api.log

# Verificar uptime
watch -n 1 curl -s http://localhost:8000/api/health

# Estadísticas de performance
ab -n 1000 -c 10 http://localhost:8000/api/products
```

---

**¡Todos los endpoints probados y funcionando! ✅**
