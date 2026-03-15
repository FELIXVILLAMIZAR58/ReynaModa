# 🎀 REYNA MODA - Estructura del Sitio (ACTUALIZADO)

## 📋 Páginas Disponibles

### 1. **PÁGINA PRINCIPAL** (`/`)
- **URL**: `http://localhost:8000/`
- **Contenido**:
  - Hero section con titulo animado "LUCE COMO UNA REYNA"
  - Corona SVG elegante con animación de flotación
  - Sección de características (Calidad, Diseños, Tendencias)
  - Productos destacados con filtros
  - Sección CTA (Call to Action)
  - Sección de contacto

### 2. **CATÁLOGO** (`/catalog.html`)
- **URL**: `http://localhost:8000/catalog.html`
- **Contenido**:
  - Página completa dedicada al catálogo de productos
  - Filtros por categoría (Todos, Vestidos, Blusas, Pantalones, Accesorios)
  - Grid de productos con 12+ items de demostración
  - Carrito de compras integrado
  - Sistema de ofertas y badges

### 3. **PANEL DE ADMINISTRACIÓN** (`/admin`)
- **URL**: `http://localhost:8000/admin`
- **Credenciales**:
  - Usuario: `admin`
  - Contraseña: `ReynaAdmin2025`
- **Funcionalidades**:
  - ✨ Tabs: Redes Sociales, Productos, Órdenes, Analytics
  - 🌐 Gestión de Instagram, TikTok, WhatsApp
  - 🤖 Generador de videos con IA
  - 📱 Notificaciones automáticas en WhatsApp
  - 📦 Gestión de productos (próxima)
  - 📋 Gestión de órdenes (próxima)
  - 📊 Analytics (próxima)

---

## 🎛️ PANEL DE USUARIO

### Ubicación
- **En el header de todas las páginas** (icono 👤 esquina superior derecha)

### Funcionalidades
1. **Invitado** (por defecto):
   - Ver: "Invitado"
   - Opción: "Iniciar Sesión"

2. **Usuario Autenticado**:
   - Ver: "Hola, [usuario]"
   - Acceso: Link a "Panel Admin"
   - Opción: "Cerrar Sesión"

### Flujo de Inicio de Sesión
1. Click en icono 👤
2. Click en "Iniciar Sesión"
3. Se abre modal con formulario
4. Ingresa credenciales:
   - Usuario: `admin`
   - Contraseña: `ReynaAdmin2025`
5. Click en "Ingresar"
6. Token se guarda en localStorage
7. Panel se actualiza automáticamente

---

## 🌐 PANEL DE REDES SOCIALES (NUEVO)

### Acceso
- **Admin Panel** → Tab "Redes Sociales"

### Configuraciones

#### 📸 Instagram
- Token de acceso Meta Graph API
- ID de Cuenta Business
- Publicación automática de contenido

#### 🎵 TikTok
- Token de acceso API
- ID de Cuenta
- Publicación automática de videos

#### 💬 WhatsApp Business
- Token de acceso WhatsApp
- Número de Teléfono ID
- Notificaciones automáticas en compras

#### 🤖 Generador IA de Contenido
- Clave API (OpenAI, Anthropic, etc.)
- Selección de modelo (GPT-4, Claude, etc.)
- Autogeneración de descripción y captions

#### 🎬 Generador de Videos IA
- ID del Producto
- Tipo de video:
  - **Product-Showcase**: Presentación elegante
  - **Testimonial**: Testimonio de clienta
  - **Promo**: Promoción con oferta
  - **Trend**: Video viral trending
- Genera y publica automáticamente en Instagram y TikTok

---

## 🛒 CARRITO DE COMPRAS

### Disponible en:
- Página principal (`/`)
- Catálogo (`/catalog.html`)

### Características:
- Icono 🛍️ en el header con contador
- Modal con lista de productos
- Cálculo automático de totales + envío
- Opción de proceder al pago
- Datos persisten en localStorage
- Botón para eliminar productos

---

## 🎨 DISEÑO (ACTUALIZADO)

### Colores Elegantes
- **Primario**: Dorado `#C9A961` (cálido y sofisticado)
- **Primario Claro**: Beige `#E8D4B0` (hover effects)
- **Acento**: Dorado Oscuro `#D4A574` (gradientes)
- **Fondo Premium**: `#1a1a1a` y `#2d2d2d` (gradientes elegantes)

### Tipografía Corporativa
- **Headings**: Playfair Display (Google Fonts) - Elegante y premium
- **Body**: Poppins (Google Fonts) - Moderno y corporativo
- **Efecto**: Profesional, sofisticado, NO plano

### Elementos Visuales
- **Corona**: SVG elegante con animación de flotación
- **Botones**: Gradientes suaves con sombras
- **Transiciones**: cubic-bezier (suave y profesional)
- **Hover Effects**: Transformaciones y brillos

### Responsivo
- Desktop: Completo y elegante
- Tablet: Adaptado
- Mobile: Optimizado

---

## 🔗 NAVEGACIÓN

### Header
- Logo "✨ REYNA MODA" (con brillo)
- Menú: INICIO | CATÁLOGO | CONTACTO
- Carrito 🛍️ con contador
- Panel de Usuario 👤 con dropdown

### Footer
- Copyright
- Información de la marca

---

## 💾 ALMACENAMIENTO

### LocalStorage
- `reyna_cart`: Carrito de compras (JSON)
- `reyna_admin_token`: Token JWT
- `reyna_admin_user`: Nombre de usuario
- `social_instagram`: Config Instagram
- `social_tiktok`: Config TikTok
- `social_whatsapp`: Config WhatsApp
- `social_llm`: Config IA

### MongoDB (Servidor)
- `social_config`: Credenciales de plataformas
- `generated_videos`: Historial de videos
- `social_posts`: Posts publicados
- `products`: Catálogo
- `orders`: Pedidos
- `admins`: Usuarios

---

## 🚀 RUTAS API (Backend)

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrarse
- `GET /api/auth/me` - Datos del usuario

### Productos
- `GET /api/products` - Listar todos
- `POST /api/products` - Crear (admin)
- `PUT /api/products/{id}` - Actualizar (admin)
- `DELETE /api/products/{id}` - Eliminar (admin)

### Órdenes
- `GET /api/orders` - Listar todas
- `POST /api/orders` - Crear orden
- `PUT /api/orders/{id}` - Actualizar estado (admin)

### Redes Sociales (NUEVO)
- `POST /api/social/config` - Guardar configuración
- `GET /api/social/config/{platform}` - Obtener config
- `POST /api/ai/generate-video` - Generar video con IA
- `POST /api/orders/{id}/notify-customer` - Notificar compra

### Analytics
- `GET /api/analytics` - Estadísticas del dashboard

---

## 📊 DATOS DE DEMOSTRACIÓN

El sistema incluye 12 productos:
1. Vestido Negro Elegante - Vestidos - $85,000 → $65,000
2. Blusa Dorada Brillante - Blusas - $45,000
3. Pantalón Blanco Ajustado - Pantalones - $55,000 → $40,000
4. Collar Dorado Premium - Accesorios - $25,000
5. Vestido Rojo Pasión - Vestidos - $95,000 → $75,000
6. Blusa Transparente Negra - Blusas - $38,000
7. Pantalón Negro Elegante - Pantalones - $65,000
8. Aretes Dorados Luxury - Accesorios - $18,000
9. Vestido Azul Marino - Vestidos - $75,000
10. Blusa Rosa Pastel - Blusas - $42,000 → $32,000
11. Pantalón Beige Clásico - Pantalones - $58,000
12. Bolso Dorado Pequeño - Accesorios - $35,000

---

## ✨ CARACTERÍSTICAS PRINCIPALES

### Página Principal
- ✅ Hero elegante con corona animada
- ✅ Gradientes premium
- ✅ Tipografía corporativa
- ✅ Botones con efectos sofisticados
- ✅ Grid de productos responsive

### Catálogo
- ✅ Página dedicada
- ✅ Filtros por categoría
- ✅ Sistema de ofertas
- ✅ Carrito persistente
- ✅ Diseño elegante

### Panel Admin
- ✅ Login seguro JWT
- ✅ Configuración de redes sociales
- ✅ Generador IA de videos
- ✅ Notificaciones WhatsApp
- ✅ Tabs organizados

### Panel de Usuario
- ✅ Login/Logout
- ✅ Acceso a admin
- ✅ Dropdown menu
- ✅ Estado persistente

### Seguridad
- ✅ Contraseñas encriptadas (bcrypt)
- ✅ Tokens JWT
- ✅ Validación en backend
- ✅ CORS habilitado

---

## ✅ ESTADO ACTUAL

- ✅ Página principal completa y elegante
- ✅ Página de catálogo separada
- ✅ Panel de usuario con login
- ✅ Carrito de compras
- ✅ Panel de administración
- ✅ Gestión de redes sociales
- ✅ Generador IA de videos
- ✅ Notificaciones WhatsApp
- ✅ Integración API
- ✅ Responsive design
- ✅ LocalStorage persistence
- ✅ Paleta de colores elegante
- ✅ Tipografía corporativa
- ✅ Corona rediseñada

---

## 🎯 Credenciales

```
Usuario: admin
Contraseña: ReynaAdmin2025
```

## 🌍 URLs Principales

```
Inicio: http://localhost:8000/
Catálogo: http://localhost:8000/catalog.html
Admin: http://localhost:8000/admin
API Docs: http://localhost:8000/docs
```

---

**¡REYNA MODA está listo para brillar! ✨👑**

