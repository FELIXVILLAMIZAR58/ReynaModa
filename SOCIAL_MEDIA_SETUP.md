# 🚀 REYNA MODA — Guía de Instalación del Módulo Social Media

## ✅ Costo total: $0

| Servicio            | Costo     | Límite gratuito              |
|---------------------|-----------|------------------------------|
| Instagram Graph API | Gratis    | Sin límite de publicaciones  |
| WhatsApp Cloud API  | Gratis    | 1000 conversaciones/mes      |
| rembg (fondo IA)    | Gratis    | Sin límite, corre en tu PC   |
| APScheduler         | Gratis    | Sin límite                   |
| TikTok (semi-auto)  | Gratis    | Sin aprobación necesaria     |

---

## PASO 1 — Actualizar dependencias del backend

```bash
cd /app/backend
pip install -r requirements.txt
```

Nuevas dependencias agregadas:
- `apscheduler` — publicaciones programadas
- `rembg` — remover fondo de imágenes (gratis, local)
- `httpx` — cliente HTTP async

---

## PASO 2 — Reemplazar archivos

Copia los archivos a tu proyecto:

```
backend/
  server.py          → reemplaza el actual
  requirements.txt   → reemplaza el actual
  .env               → agrega las nuevas variables (no borres las existentes)

frontend/src/pages/
  AdminDashboard.js  → reemplaza el actual
  SocialMedia.js     → archivo NUEVO (agrégalo)
```

---

## PASO 3 — Conectar Instagram (cuando quieras, no es urgente)

### 3a. Crear app en Meta Developers (gratis)

1. Ve a https://developers.facebook.com
2. Crea una nueva app → tipo "Business"
3. Agrega el producto "Instagram Graph API"
4. En "Roles" → agrega tu cuenta de Instagram
5. Genera un Access Token con permisos:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`

### 3b. Obtener el Business Account ID

```
GET https://graph.facebook.com/v19.0/me/accounts?access_token=TU_TOKEN
```
Copia el `id` de tu página de Facebook → úsalo para obtener el IG ID:
```
GET https://graph.facebook.com/v19.0/{page_id}?fields=instagram_business_account&access_token=TU_TOKEN
```

### 3c. Guardar en el panel

Ve a: Admin → Social → Cuentas → Instagram → pega el token y el ID → Guardar.

---

## PASO 4 — WhatsApp Cloud API (cuando tengas pedidos regulares)

### 4a. En la misma app de Meta Developers

1. Agrega el producto "WhatsApp"
2. Ve a "Configuración" de WhatsApp
3. Copia el **Phone Number ID** (número de prueba gratuito disponible)
4. Genera un token de acceso permanente

### 4b. Número de teléfono

**Importante:** El número de WhatsApp API NO puede ser el mismo que ya usas
en WhatsApp normal. Opciones:
- Usar un número nuevo/SIM extra
- Usar el número de prueba que Meta da gratis para desarrollo

### 4c. Guardar en el panel

Ve a: Admin → Social → Cuentas → WhatsApp → pega los datos → Guardar.

**Sin configurar:** el sistema sigue funcionando con links wa.me (igual que hoy). 
La API solo agrega confirmaciones automáticas.

---

## PASO 5 — TikTok (ya funciona sin configurar)

No requiere ninguna configuración. Flujo automático:

1. En Admin → Social → Crear con IA → genera el caption
2. En Programar → selecciona TikTok → Publicar
3. El sistema envía el contenido a tu WhatsApp (3167470857)
4. Abres TikTok en tu celular → pegas el texto → publicas

---

## PASO 6 — Probar que todo funciona

```bash
# Health check
curl http://localhost:8001/api/health

# Ver estado de redes sociales
curl -H "Authorization: Bearer TU_TOKEN" http://localhost:8001/api/social/status

# Generar contenido de prueba
curl -X POST http://localhost:8001/api/social/generate-content \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productName":"Vestido Gala Nocturna","category":"Mujer","price":150000,"contentType":"post","tone":"elegant","tags":["oferta"]}'
```

---

## Nuevos endpoints disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/social/status` | GET | Estado de cuentas conectadas |
| `/api/social/connect/instagram` | POST | Guardar token Instagram |
| `/api/social/connect/whatsapp` | POST | Guardar config WhatsApp |
| `/api/social/generate-content` | POST | Generar caption + hashtags con IA |
| `/api/social/publish/instagram` | POST | Publicar en Instagram |
| `/api/social/publish/whatsapp` | POST | Enviar por WhatsApp |
| `/api/social/prepare/tiktok` | POST | Preparar contenido TikTok |
| `/api/social/schedule` | POST | Programar publicación futura |
| `/api/social/scheduled` | GET | Ver publicaciones programadas |
| `/api/social/history` | GET | Historial de publicaciones |
| `/api/social/stats` | GET | Estadísticas |
| `/api/social/remove-background` | POST | Remover fondo (upload) |
| `/api/social/remove-background-url` | POST | Remover fondo (URL) |
| `/api/orders/{id}/notify-whatsapp` | POST | Notificar pedido al cliente |

---

## Navegación en el panel

La nueva pestaña **"Social"** aparece en el menú lateral del admin:
```
Dashboard | Productos | Pedidos | Social ← NUEVO
```

Dentro de Social:
- **Cuentas** — conectar Instagram, WhatsApp, ver estado TikTok
- **Crear con IA** — generar captions, hashtags, remover fondo
- **Programar** — calendario de publicaciones
- **Historial** — registro de todo lo publicado

---

*© 2026 REYNA MODA — Módulo Social Media v2.0*
