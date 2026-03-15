# 🏗️ REYNA MODA - ARQUITECTURA COMPLETA

## 📦 ESTRUCTURA DEL PROYECTO

```
reyna-moda/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app principal
│   │   ├── config.py                  # Configuración
│   │   ├── database.py                # Conexión Firestore
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # Autenticación
│   │   │   ├── products.py            # Gestión de productos
│   │   │   ├── orders.py              # Gestión de órdenes
│   │   │   ├── payments.py            # Pagos
│   │   │   ├── cart.py                # Carrito
│   │   │   ├── analytics.py           # Analytics
│   │   │   ├── admin.py               # Panel admin
│   │   │   ├── ai_marketing.py        # Agente IA Marketing
│   │   │   ├── social_media.py        # TikTok + Instagram
│   │   │   ├── chatbot.py             # Chatbot IA
│   │   │   └── shipping.py            # Cálculo de envíos
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   ├── inventory.py
│   │   │   └── analytics.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── email_service.py
│   │   │   ├── storage_service.py     # Firebase Storage
│   │   │   ├── ai_service.py          # Servicios IA
│   │   │   ├── video_generator.py     # Generador de videos
│   │   │   ├── payment_service.py     # Procesar pagos
│   │   │   ├── shipping_service.py    # Cálculo de envíos
│   │   │   └── seo_service.py         # SEO generado
│   │   ├── utils/
│   │   │   ├── jwt_utils.py
│   │   │   ├── validators.py
│   │   │   └── constants.py
│   │   └── middleware/
│   │       ├── auth_middleware.py
│   │       └── error_middleware.py
│   ├── requirements.txt
│   ├── .env.example
│   └── server.py                      # WSGI entry point
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   ├── Cart.jsx
│   │   │   ├── Favorites.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── Filters.jsx
│   │   │   └── Chatbot.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Catalog.jsx
│   │   │   ├── ProductDetail.jsx
│   │   │   ├── Checkout.jsx
│   │   │   ├── OrderConfirmation.jsx
│   │   │   ├── Profile.jsx
│   │   │   └── NotFound.jsx
│   │   ├── admin/
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── ProductManager.jsx
│   │   │   ├── OrderManager.jsx
│   │   │   ├── InventoryManager.jsx
│   │   │   ├── AnalyticsPanel.jsx
│   │   │   ├── AIMarketing.jsx        # Panel IA Marketing
│   │   │   ├── SocialMediaManager.jsx # Gestor Redes Sociales
│   │   │   └── UserManager.jsx
│   │   ├── hooks/
│   │   │   ├── useCart.js
│   │   │   ├── useFavorites.js
│   │   │   ├── useAuth.js
│   │   │   ├── useProducts.js
│   │   │   └── useOrders.js
│   │   ├── context/
│   │   │   ├── CartContext.js
│   │   │   ├── AuthContext.js
│   │   │   └── UIContext.js
│   │   ├── styles/
│   │   │   ├── global.css
│   │   │   ├── variables.css
│   │   │   └── responsive.css
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   ├── products.js
│   │   │   ├── orders.js
│   │   │   ├── payments.js
│   │   │   └── chat.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── admin-panel/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Products/
│   │   │   ├── Orders/
│   │   │   ├── Inventory/
│   │   │   ├── Analytics/
│   │   │   ├── Users/
│   │   │   ├── AIMarketing/
│   │   │   └── Settings/
│   │   ├── components/
│   │   ├── styles/
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   ├── ARQUITECTURA.md
│   ├── API_DOCS.md
│   ├── INSTALACION.md
│   ├── CONFIGURACION.md
│   └── DEPLOYMENT.md
│
└── docker-compose.yml
```

---

## 🗄️ BASE DE DATOS (FIRESTORE)

### Colecciones

#### 1. **users**
```json
{
  "id": "user_001",
  "email": "customer@example.com",
  "name": "Maria García",
  "phone": "573001234567",
  "avatar": "https://storage.googleapis.com/...",
  "role": "customer", // "customer", "admin"
  "addresses": [
    {
      "id": "addr_001",
      "city": "Bucaramanga",
      "state": "Santander",
      "street": "Calle 45 #23-45",
      "zipCode": "680001",
      "isDefault": true
    }
  ],
  "favorites": ["prod_001", "prod_002"],
  "orders": ["order_001"],
  "createdAt": "2026-03-14T00:00:00Z",
  "lastLogin": "2026-03-14T10:30:00Z",
  "isActive": true
}
```

#### 2. **products**
```json
{
  "id": "prod_001",
  "name": "Vestido Negro Elegante",
  "description": "Vestido negro de gala, tela premium de poliéster",
  "price": 89.99,
  "salePrice": 69.99,
  "category": "vestidos",
  "sizes": ["XS", "S", "M", "L", "XL"],
  "colors": ["negro", "rojo", "blanco"],
  "stock": 25,
  "images": [
    "https://storage.googleapis.com/.../img1.jpg",
    "https://storage.googleapis.com/.../img2.jpg"
  ],
  "video": "https://storage.googleapis.com/.../video.mp4",
  "tags": ["nuevo", "oferta", "tendencia"],
  "seo": {
    "title": "Vestido Negro Elegante - REYNA MODA",
    "description": "Compra nuestro vestido negro elegante",
    "keywords": "vestido, negro, elegante, gala"
  },
  "rating": 4.8,
  "reviews": 45,
  "active": true,
  "createdAt": "2026-03-14T00:00:00Z",
  "updatedAt": "2026-03-14T00:00:00Z"
}
```

#### 3. **orders**
```json
{
  "id": "order_001",
  "userId": "user_001",
  "items": [
    {
      "productId": "prod_001",
      "productName": "Vestido Negro Elegante",
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
  "payment": {
    "method": "nequi", // "nequi", "transfer", "cash_on_delivery"
    "status": "completed",
    "transactionId": "tx_001",
    "amount": 74.99
  },
  "status": "pending", // "pending", "processing", "shipped", "delivered", "cancelled"
  "total": 74.99,
  "notes": "Entregar después de las 5 PM",
  "createdAt": "2026-03-14T10:30:00Z",
  "updatedAt": "2026-03-14T10:30:00Z"
}
```

#### 4. **inventory**
```json
{
  "id": "inv_001",
  "productId": "prod_001",
  "totalStock": 100,
  "available": 75,
  "reserved": 20,
  "damaged": 5,
  "lowStockAlert": 20,
  "reorderLevel": 30,
  "lastRestocked": "2026-03-10T00:00:00Z",
  "warehouse": "Bucaramanga"
}
```

#### 5. **analytics**
```json
{
  "id": "analytics_daily_2026_03_14",
  "date": "2026-03-14",
  "metrics": {
    "visits": 1250,
    "uniqueVisitors": 850,
    "pageViews": 3400,
    "ordersCreated": 25,
    "totalRevenue": 1875.50,
    "avgOrderValue": 75.02,
    "conversionRate": 2.94,
    "cartAbandonmentRate": 45.2
  },
  "topProducts": [
    {"id": "prod_001", "sales": 5},
    {"id": "prod_002", "sales": 4}
  ],
  "traffic": {
    "organic": 450,
    "direct": 200,
    "social": 150,
    "paid": 50
  }
}
```

#### 6. **marketing_content**
```json
{
  "id": "mc_001",
  "productId": "prod_001",
  "type": "instagram_post",
  "content": {
    "caption": "Este vestido elegante está diseñado...",
    "hashtags": ["#ReynaM oda", "#ModaLujo"],
    "image": "https://storage.googleapis.com/.../insta.jpg",
    "video": null
  },
  "platforms": ["instagram", "facebook"],
  "status": "published",
  "publishedAt": "2026-03-14T10:00:00Z",
  "engagement": {
    "likes": 234,
    "comments": 12,
    "shares": 5
  }
}
```

---

## 🔌 RUTAS API

### Autenticación
- `POST /api/auth/register` - Registrarse
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/logout` - Cerrar sesión
- `POST /api/auth/refresh` - Refrescar token
- `GET /api/auth/me` - Obtener datos del usuario

### Productos
- `GET /api/products` - Listar todos (con filtros)
- `GET /api/products/{id}` - Detalle del producto
- `POST /api/products` - Crear (admin)
- `PUT /api/products/{id}` - Actualizar (admin)
- `DELETE /api/products/{id}` - Eliminar (admin)
- `GET /api/products/search` - Búsqueda

### Carrito
- `GET /api/cart` - Obtener carrito
- `POST /api/cart/add` - Agregar al carrito
- `PUT /api/cart/update` - Actualizar cantidad
- `DELETE /api/cart/remove` - Eliminar del carrito
- `DELETE /api/cart/clear` - Vaciar carrito

### Órdenes
- `POST /api/orders` - Crear orden
- `GET /api/orders` - Mis órdenes
- `GET /api/orders/{id}` - Detalle de orden
- `PUT /api/orders/{id}/status` - Cambiar estado (admin)
- `GET /api/admin/orders` - Todas las órdenes (admin)

### Pagos
- `POST /api/payments/nequi` - Pagar con Nequi
- `POST /api/payments/transfer` - Transferencia bancaria
- `POST /api/payments/verify` - Verificar pago
- `POST /api/payments/webhooks` - Webhooks de pago

### Envíos
- `POST /api/shipping/calculate` - Calcular costo de envío
- `GET /api/shipping/cities` - Listar ciudades

### IA Marketing
- `POST /api/ai/enhance-image` - Mejorar imagen
- `POST /api/ai/generate-video` - Generar video promocional
- `POST /api/ai/generate-copy` - Generar copy
- `POST /api/ai/auto-publish` - Publicar automáticamente

### Redes Sociales
- `POST /api/social/instagram/publish` - Publicar en Instagram
- `POST /api/social/tiktok/publish` - Publicar en TikTok
- `GET /api/social/instagram/feed` - Obtener feed
- `GET /api/social/tiktok/videos` - Obtener videos

### Chatbot
- `POST /api/chat/message` - Enviar mensaje
- `GET /api/chat/history` - Historial de chat

### Analítica
- `GET /api/analytics/dashboard` - Dashboard analytics
- `GET /api/analytics/products` - Productos más vendidos
- `GET /api/analytics/revenue` - Ingresos
- `GET /api/analytics/customers` - Clientes frecuentes

### Admin
- `GET /api/admin/dashboard` - Dashboard admin
- `GET /api/admin/inventory` - Gestión inventario
- `POST /api/admin/users` - Crear usuario
- `PUT /api/admin/users/{id}` - Actualizar usuario
- `DELETE /api/admin/users/{id}` - Eliminar usuario

---

## 🎨 DISEÑO

### Colores
- **Primario**: Dorado `#D4AF37`
- **Acento**: Fucsia `#E91E63`
- **Fondo**: Negro `#0a0a0a`
- **Gris Claro**: `#f5f5f5`
- **Gris Oscuro**: `#1a1a1a`

### Tipografía
- **Encabezados**: 'Playfair Display'
- **Cuerpo**: 'Segoe UI', Tahoma

### Componentes UI
- Cards con hover elegantes
- Animaciones suaves
- Gradientes dorado-negro
- Efectos glassmorphism

---

## 🔐 SEGURIDAD

- ✅ JWT autenticación
- ✅ CORS habilitado
- ✅ Validación de inputs
- ✅ Protección admin
- ✅ Encriptación de contraseñas (bcrypt)
- ✅ Rate limiting
- ✅ HTTPS en producción

---

## 🚀 ESCALABILIDAD

- Preparado para múltiples vendedores
- API RESTful modulada
- Caché con Redis
- CDN para imágenes
- Serverless ready
- App móvil expandible

---

## 📊 TECNOLOGÍAS

### Backend
- FastAPI (Python)
- Firebase Firestore
- Firebase Storage
- JWT
- Redis (caché)

### Frontend
- React 18
- Vite
- Tailwind CSS
- Context API / Redux

### IA
- OpenAI GPT-4
- Stability AI (imágenes)
- Eleven Labs (voz)
- FFmpeg (videos)

### Integraciones
- Meta Graph API (Instagram)
- TikTok Developer API
- Nequi API
- SendGrid (emails)

---

## ✅ CHECKLIST DE FUNCIONALIDADES

### Tienda Online
- [ ] Catálogo con 50+ productos
- [ ] Filtros (categoría, precio, talla, popularidad)
- [ ] Búsqueda full-text
- [ ] Carrito persistente
- [ ] Favoritos
- [ ] Reviews y ratings
- [ ] Checkout optimizado
- [ ] 3 métodos de pago

### Panel Admin
- [ ] Dashboard con KPIs
- [ ] CRUD de productos
- [ ] Gestión de inventario
- [ ] Gestión de órdenes
- [ ] Usuarios admin
- [ ] Reports de ventas

### IA Marketing
- [ ] Mejora de imágenes
- [ ] Generación de videos
- [ ] Copywriting automático
- [ ] Publicaciones automáticas
- [ ] Recommendations engine

### Redes Sociales
- [ ] Publicación directa Instagram
- [ ] Publicación directa TikTok
- [ ] Programación de posts
- [ ] Analytics de engagement

### Chatbot
- [ ] Respuestas a preguntas
- [ ] Recomendaciones
- [ ] Asistencia en checkout
- [ ] Multi-idioma

---

**Fecha**: 14 de marzo de 2026
**Versión**: 2.0 - Arquitectura Premium
**Status**: 🟢 Listo para implementación
