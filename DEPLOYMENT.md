# 🚀 GUÍA DE DEPLOYMENT - REYNA MODA v2.0

## 📱 Opciones de Hosting

### Opción 1: HEROKU (Recomendado - Fácil)

#### Paso 1: Preparar proyecto
```bash
cd backend

# Crear archivo Procfile
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app" > Procfile

# Instalar gunicorn
pip install gunicorn
```

#### Paso 2: Crear app en Heroku
```bash
heroku login
heroku create reyna-moda-api
```

#### Paso 3: Agregar variables de entorno
```bash
heroku config:set JWT_SECRET_KEY=tu_secret_key
heroku config:set FIREBASE_PRIVATE_KEY=tu_key
# ... agregar todas las variables
```

#### Paso 4: Deploy
```bash
git push heroku main
```

**URL**: `https://reyna-moda-api.herokuapp.com`

---

### Opción 2: RAILWAY.APP (Moderno - Recomendado)

#### Paso 1: Conectar GitHub
1. Ir a https://railway.app
2. Login con GitHub
3. Click en "New Project"
4. Conectar repositorio

#### Paso 2: Agregar variables
- En "Variables", agregar todas las del `.env`

#### Paso 3: Deploy automático
- Cada push a `main` se despliega automáticamente

**URL**: Asignada automáticamente

---

### Opción 3: GOOGLE CLOUD RUN (Profesional)

#### Paso 1: Preparar Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Paso 2: Deploy
```bash
gcloud run deploy reyna-moda-api \
  --source . \
  --region us-central1 \
  --platform managed \
  --memory 512Mi \
  --timeout 3600 \
  --set-env-vars-from .env
```

---

### Opción 4: AWS (Profesional)

#### ECS (Elastic Container Service)
1. Crear cluster ECS
2. Crear task definition
3. Crear service
4. Configurar load balancer

#### RDS (Base de datos)
- Usar RDS para MongoDB o PostgreSQL
- Cambiar `MONGO_URL` en variables de entorno

---

### Opción 5: DIGITAL OCEAN (Balance)

#### Paso 1: Crear droplet
```bash
# Crear droplet Ubuntu 22.04
# 2GB RAM, 50GB SSD

# SSH
ssh root@YOUR_IP
```

#### Paso 2: Instalar dependencias
```bash
apt update && apt upgrade -y
apt install python3-pip python3-venv git nginx -y

# Clonar repositorio
git clone https://github.com/tu-repo/reyna-moda.git
cd reyna-moda/backend
```

#### Paso 3: Configurar app
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### Paso 4: Crear servicio systemd
```bash
sudo cat > /etc/systemd/system/reyna-moda.service << EOF
[Unit]
Description=REYNA MODA API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/root/reyna-moda/backend
Environment="PATH=/root/reyna-moda/backend/venv/bin"
ExecStart=/root/reyna-moda/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind unix:/run/gunicorn.sock

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable reyna-moda
sudo systemctl start reyna-moda
```

#### Paso 5: Configurar Nginx
```bash
sudo cat > /etc/nginx/sites-available/reyna-moda << EOF
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/reyna-moda /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Paso 6: SSL con Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

---

## 🗄️ BASE DE DATOS EN PRODUCCIÓN

### Firebase Firestore
✅ **Recomendado** - Escalable, sin server

### MongoDB Atlas
```bash
# URL de conexión
MONGO_URL=mongodb+srv://user:password@cluster.mongodb.net/reyna_moda_db

# Actualizar en código
client = AsyncIOMotorClient(MONGO_URL)
```

### PostgreSQL (Alternativa)
```bash
pip install sqlalchemy psycopg2-binary
# Cambiar ORM si es necesario
```

---

## 📧 CONFIGURAR SERVICIOS EXTERNOS

### SendGrid (Emails)
```bash
# Crear cuenta: https://sendgrid.com
# Generar API key
# En .env:
SENDGRID_API_KEY=SG.xxxxxxxx
SENDGRID_FROM_EMAIL=noreply@reynamoda.com
```

### Stripe (Pagos opcionales)
```bash
pip install stripe
# En .env:
STRIPE_PUBLIC_KEY=pk_xxx
STRIPE_SECRET_KEY=sk_xxx
```

### CloudFlare (CDN)
1. Agregar dominio a CloudFlare
2. Cambiar nameservers
3. Activar proxy/caché
4. Configurar SSL full

---

## 🚨 SEGURIDAD EN PRODUCCIÓN

### 1. Variables de entorno
```bash
# NUNCA en código
# SIEMPRE en variables del hosting
# Usar gestores de secretos:
# - AWS Secrets Manager
# - Google Cloud Secret Manager
# - HashiCorp Vault
```

### 2. CORS
```python
# Cambiar en .env
ALLOWED_ORIGINS=https://reynamoda.com,https://www.reynamoda.com
```

### 3. HTTPS
- Certificado SSL obligatorio
- Usar `https://` en todas las URLs

### 4. Rate Limiting
```python
# Ya incluido en middleware
# Configurar límites según carga
```

### 5. WAF (Web Application Firewall)
- CloudFlare
- AWS WAF
- Google Cloud Armor

---

## 📊 MONITOREO

### Sentry (Error tracking)
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

### Datadog (Performance)
```bash
pip install datadog
```

### New Relic
- Integración fácil
- APM completo

---

## 🔄 CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Run tests
      run: |
        pip install -r requirements.txt
        pytest
    
    - name: Deploy
      run: |
        git push heroku main
```

---

## 📈 ESCALABILIDAD

### Caché con Redis
```python
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Cachear productos
@app.get("/api/products")
async def get_products(skip: int = 0, limit: int = 20):
    cache_key = f"products:{skip}:{limit}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # ... obtener de DB
    # redis_client.setex(cache_key, 3600, json.dumps(data))
```

### Load Balancing
- HAProxy
- Nginx
- AWS ELB

### CDN para imágenes
- CloudFlare
- Cloudinary
- AWS CloudFront

---

## 📋 CHECKLIST PRE-LANZAMIENTO

- [ ] Variables de entorno configuradas
- [ ] Base de datos en producción
- [ ] SSL/HTTPS activado
- [ ] Dominio apuntando
- [ ] Email configurado
- [ ] Pagos testados
- [ ] Redes sociales configuradas
- [ ] Backups configurados
- [ ] Monitoreo activo
- [ ] Logs centralizados
- [ ] API documentada
- [ ] Testing completado
- [ ] Performance optimizado
- [ ] Security scan pasado

---

## 🆘 TROUBLESHOOTING

### Error 502 Bad Gateway
```bash
# Logs
heroku logs --tail
# o
docker logs container_name
```

### Base de datos no conecta
- Verificar credenciales
- Verificar IP whitelist
- Verificar connection string

### CORS error
- Verificar ALLOWED_ORIGINS
- Verificar headers en respuesta

### Rate limiting
- Aumentar límites
- Implementar caché

---

## 📞 SOPORTE EN PRODUCCIÓN

### Uptime Monitoring
- Pingdom
- StatusCake
- UptimeRobot

### On-call
- PagerDuty
- OpsGenie

### Incident Response
- Runbooks
- Playbooks
- Postmortem analysis

---

**¡Tu REYNA MODA está lista para el mundo! 🚀**
