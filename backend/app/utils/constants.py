# 🎨 Constantes de la aplicación

# Categorías de productos
PRODUCT_CATEGORIES = [
    "vestidos",
    "blusas",
    "pantalones",
    "accesorios",
    "faldas",
    "chaquetas",
    "zapatos"
]

# Etiquetas de productos
PRODUCT_TAGS = [
    "nuevo",
    "oferta",
    "tendencia",
    "best-seller",
    "agotado",
    "limitado"
]

# Tallas disponibles
AVAILABLE_SIZES = [
    "XS", "S", "M", "L", "XL", "XXL", "XXXL",
    "32", "34", "36", "38", "40", "42", "44", "46"
]

# Colores disponibles
AVAILABLE_COLORS = [
    "negro", "blanco", "rojo", "azul", "verde", "amarillo",
    "rosa", "morado", "gris", "beige", "dorado", "plateado",
    "naranja", "turquesa", "marrón", "fucsia"
]

# Estados de orden
ORDER_STATUSES = [
    "pending",      # Pendiente de pago
    "processing",   # En proceso
    "shipped",      # Enviado
    "delivered",    # Entregado
    "cancelled"     # Cancelado
]

# Métodos de pago
PAYMENT_METHODS = [
    "nequi",
    "transfer",
    "cash_on_delivery"
]

# Estados de pago
PAYMENT_STATUSES = [
    "pending",
    "completed",
    "failed",
    "refunded"
]

# Roles de usuario
USER_ROLES = [
    "customer",
    "admin",
    "vendor"
]

# Ciudades de envío local (menor costo)
LOCAL_CITIES = [
    "Bucaramanga",
    "Floridablanca",
    "Girón",
    "Piedecuesta"
]

# Tamaños mínimos y máximos
MIN_PRICE = 0.01
MAX_PRICE = 999999.99
MIN_STOCK = 0
MAX_STOCK = 999999

# Paginación
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Límites de carga
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/webm"]

# Cache
CACHE_TTL_PRODUCTS = 3600  # 1 hora
CACHE_TTL_ORDERS = 600    # 10 minutos
CACHE_TTL_ANALYTICS = 1800  # 30 minutos
