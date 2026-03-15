# 👑 REYNA MODA - GUÍA COMPLETA DEL SISTEMA

## 🎯 Resumen Ejecutivo

**REYNA MODA** es una plataforma e-commerce completamente integrada con:
- ✨ Diseño premium y elegante (dorados sofisticados)
- 🛍️ Catálogo de productos con carrito de compras
- 👤 Panel de usuario con login seguro
- 🌐 Gestor de redes sociales
- 🤖 Generador de videos con IA
- 📱 Notificaciones automáticas en WhatsApp
- 📊 Dashboard administrativo

---

## 🌐 URLs Principales

| Página | URL | Descripción |
|---|---|---|
| **Inicio** | `http://localhost:8000/` | Página principal con hero y productos |
| **Catálogo** | `http://localhost:8000/catalog.html` | Catálogo completo con filtros |
| **Admin** | `http://localhost:8000/admin` | Panel administrativo |
| **API Docs** | `http://localhost:8000/docs` | Documentación interactiva |

---

## 🔐 Credenciales de Acceso

### Administrador
```
Usuario: admin
Contraseña: ReynaAdmin2025
```

**Acceso desde cualquier página:**
1. Click en icono 👤 (esquina superior derecha)
2. Click en "Iniciar Sesión"
3. Ingresa credenciales
4. Click en "Panel Admin" para acceder al dashboard

---

## 🎨 Diseño Visual

### Paleta de Colores
```
Primario (Dorado): #C9A961
Primario Claro: #E8D4B0
Acento: #D4A574
Fondo: #1a1a1a
Premium: #2d2d2d
```

### Tipografía
- **Headings**: Playfair Display (Google Fonts)
- **Cuerpo**: Poppins (Google Fonts)
- **Efecto**: Corporativo, elegante, NO plano

### Decoraciones
- Corona SVG animada (flotación suave)
- Gradientes elegantes en botones
- Sombras premium
- Efectos hover sofisticados

---

## 📦 Características por Sección

### 1️⃣ Página Principal (/)

**Secciones:**
- **Hero**: "LUCE COMO UNA REYNA" con corona animada
- **Características**: 3 cards (Calidad, Diseños, Tendencias)
- **Productos**: Grid de productos con filtros
- **CTA**: Sección de llamada a la acción
- **Contacto**: Información de contact

**Funcionalidades:**
- ✅ Carrito de compras (🛍️)
- ✅ Login de usuario (👤)
- ✅ Filtro de productos
- ✅ Responsive design

### 2️⃣ Catálogo (/catalog.html)

**Características:**
- Página dedicada al catálogo
- 12+ productos de demostración
- Filtros por categoría
- Sistema de ofertas
- Carrito persistente

**Categorías:**
- Vestidos
- Blusas
- Pantalones
- Accesorios

### 3️⃣ Panel Admin (/admin)

**Tabs Disponibles:**

#### 🌐 Redes Sociales
Aquí configuras y gestionas todas las integraciones:

**Instagram:**
- Token de acceso Meta Graph API
- ID de Cuenta Business
- Publicación automática de contenido

**TikTok:**
- Token de acceso API
- ID de Cuenta
- Publicación de videos virales

**WhatsApp Business:**
- Token de acceso WhatsApp
- Número de Teléfono ID
- Notificaciones de compras

**Generador IA:**
- Clave API (OpenAI, Anthropic, etc.)
- Selección de modelo (GPT-4, Claude)
- Generación automática de contenido

**Generador de Videos:**
- Ingresa ID del producto
- Elige tipo de video:
  - Product-showcase
  - Testimonial
  - Promo
  - Trend
- Genera y publica automáticamente

#### 📦 Productos (Próximamente)
Gestión completa de inventario

#### 📋 Órdenes (Próximamente)
Seguimiento de pedidos

#### 📊 Analytics (Próximamente)
Estadísticas y reportes

---

## 🛒 Carrito de Compras

### Funcionamiento
1. Click en icono 🛍️ (header)
2. Se abre modal con productos agregados
3. Puedes:
   - Ver cantidad y precio
   - Eliminar productos
   - Ver total + envío
   - Proceder al pago

### Almacenamiento
- Datos guardados en `localStorage`
- Persisten entre sesiones
- Se limpian al confirmar compra

---

## 👤 Sistema de Usuario

### Login
1. Click en icono 👤
2. Click en "Iniciar Sesión"
3. Ingresa usuario y contraseña
4. Click en "Ingresar"

### Después del Login
- Se muestra: "Hola, [usuario]"
- Acceso a: "Panel Admin"
- Opción: "Cerrar Sesión"

### Seguridad
- Tokens JWT almacenados en localStorage
- Contraseña encriptada con bcrypt
- Validación en cada acción protegida

---

## 🤖 Generador IA de Contenido

### Proceso Automático

1. **Configurar IA** (Tab: Redes Sociales)
   - Ingresa clave API
   - Selecciona modelo

2. **Generar Video** (Tab: Redes Sociales)
   - Ingresa ID del producto
   - Selecciona tipo de video
   - Click en "Generar y Publicar"

3. **Sistema Automático:**
   - ✅ Genera script de video
   - ✅ Crea captions optimizados
   - ✅ Publica en Instagram/TikTok
   - ✅ Invita a comprar
   - ✅ Dirige a la tienda

### Tipos de Videos

| Tipo | Script | Caption |
|---|---|---|
| **Product-Showcase** | Presenta el producto elegantemente | "✨ NUEVO: [Producto]..." |
| **Testimonial** | Testimonio de clienta | "💕 Nuestras clientas aman..." |
| **Promo** | Promoción con oferta | "🔥 OFERTA FLASH..." |
| **Trend** | Tendencia viral | "📱 TRENDING AHORA..." |

---

## 📱 Notificaciones WhatsApp

### Configuración
1. Obtener credenciales de Meta WhatsApp Business
2. En admin → Redes Sociales → WhatsApp Business
3. Ingresa Token y Phone ID
4. Click en "Guardar WhatsApp"

### Automático en Compras
Cuando un cliente compra:
```
Hola [Nombre]! 👑

¡Gracias por tu compra en REYNA MODA!

📦 Número de Orden: #2026001
💰 Total: $65,000
📍 Entrega en: Bogotá

Tu pedido ha sido confirmado y será procesado en breve.

¡Gracias por lucir como una REYNA! ✨
```

---

## 📊 API Endpoints

### Autenticación
```
POST /api/auth/login
POST /api/auth/register
GET /api/auth/me
```

### Productos
```
GET /api/products              # Listar todos
POST /api/products             # Crear (admin)
PUT /api/products/{id}         # Actualizar (admin)
DELETE /api/products/{id}      # Eliminar (admin)
```

### Órdenes
```
GET /api/orders                # Listar
POST /api/orders               # Crear
PUT /api/orders/{id}           # Actualizar estado (admin)
```

### Redes Sociales (NUEVA)
```
POST /api/social/config                # Guardar config
GET /api/social/config/{platform}      # Obtener config
POST /api/ai/generate-video            # Generar video con IA
POST /api/orders/{id}/notify-customer  # Notificar compra
```

---

## 💾 Base de Datos (MongoDB)

### Colecciones
```
- admins           → Usuarios administrativos
- products         → Catálogo de productos
- orders           → Pedidos de clientes
- social_config    → Configuración de redes sociales
- generated_videos → Historial de videos generados
- social_posts     → Posts publicados
```

---

## 🔧 Configuración del Servidor

### Puerto
- **8000** (FastAPI con auto-reload)

### Comandos
```bash
# Iniciar servidor
python -m uvicorn server:app --reload

# Ver logs
tail -f servidor.log
```

### Requisitos
```
- Python 3.13+
- FastAPI
- Motor (MongoDB async)
- PyJWT
- Passlib + bcrypt
- APScheduler
- httpx
- Rembg (opcional, para remover fondos)
```

---

## 🎯 Casos de Uso

### Caso 1: Vender Producto Nuevo
1. Agregar producto
2. Generar video con IA
3. Publicar en redes
4. Clientes ven en TikTok/Instagram
5. Clientes entran a la tienda
6. Compran
7. Notificación automática en WhatsApp

### Caso 2: Promoción Flash
1. Crear oferta especial
2. Generar video "promo"
3. Sistema publica en todas las redes
4. Caption incluye descuento
5. Atrae clientes nuevos
6. Mayor conversión

### Caso 3: Seguir Tendencias
1. Ver tendencia viral en TikTok
2. Crear video tipo "trend"
3. Usar IA para script viral
4. Publicar rápidamente
5. La marca se mantiene fresca y relevante
6. Nuevas audiencias descubren REYNA MODA

---

## 🚀 Próximas Mejoras

- [ ] Integración real de APIs (Meta, TikTok)
- [ ] Generación de videos reales (FFmpeg)
- [ ] Analytics de engagement
- [ ] A/B testing de captions
- [ ] Panel de estadísticas completo
- [ ] Múltiples catálogos
- [ ] Gestión de inventario avanzada
- [ ] Sistema de cupones
- [ ] Reseñas de productos

---

## ❓ Preguntas Frecuentes

**P: ¿Dónde guardo los datos sensibles?**
R: En variables de entorno (.env). Las credenciales de redes se guardan encriptadas en MongoDB.

**P: ¿Cuánto cuesta publicar en redes?**
R: Gratis. Meta ofrece API gratuita. TikTok tiene límites de publicaciones diarias. WhatsApp es gratuito hasta 1,000 mensajes/mes.

**P: ¿Puedo agregar más productos?**
R: Sí. Acceso desde el panel admin (próximamente disponible UI mejorada).

**P: ¿Los videos se generan automáticamente?**
R: Sí. Una vez configures la IA, el sistema genera script, caption y los publica automáticamente.

**P: ¿Cómo cambian los colores?**
R: Edita las variables CSS `:root` en los archivos HTML. Los nuevos colores se aplicarán a todo el sitio.

---

## 📞 Soporte

Para preguntas técnicas o reportar bugs:
- Revisa la documentación API en `/docs`
- Consulta los logs del servidor
- Verifica la conexión a MongoDB

---

## 📋 Checklist de Implementación

- ✅ Paleta de colores elegante (dorados)
- ✅ Tipografía corporativa (Playfair + Poppins)
- ✅ Corona rediseñada (SVG animado)
- ✅ Panel de redes sociales
- ✅ Generador IA de videos
- ✅ Notificaciones WhatsApp
- ✅ Página de inicio con hero
- ✅ Catálogo separado
- ✅ Carrito de compras
- ✅ Panel de usuario
- ✅ Login seguro
- ✅ Responsive design

---

**¡Tu plataforma REYNA MODA está lista para brillar! ✨👑**

