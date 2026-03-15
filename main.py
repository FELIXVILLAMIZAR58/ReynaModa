from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId
import cloudinary, cloudinary.uploader
import os, jwt, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URL         = os.environ.get("MONGO_URL", "")
DB_NAME           = os.environ.get("DB_NAME", "reyna_moda_db")
JWT_SECRET        = os.environ.get("JWT_SECRET", "reyna_jwt_2025")
CLOUDINARY_CLOUD  = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_KEY    = os.environ.get("CLOUDINARY_API_KEY", "")
CLOUDINARY_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "")
ADMIN_USERS = {
    "admin":             os.environ.get("ADMIN_PASSWORD",  "ReynaAdmin2025"),
    "felixvillamizar58": os.environ.get("ADMIN_PASSWORD2", "1095809748*"),
}

cloudinary.config(cloud_name=CLOUDINARY_CLOUD, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, secure=True)
mongo_client = AsyncIOMotorClient(MONGO_URL) if MONGO_URL else None
db = mongo_client[DB_NAME] if mongo_client else None

app = FastAPI(title="REYNA MODA API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
security = HTTPBearer(auto_error=False)

def sid(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def make_token(u):
    return jwt.encode({"sub": u, "exp": datetime.utcnow() + timedelta(hours=24)}, JWT_SECRET, algorithm="HS256")

def auth(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not creds: raise HTTPException(401, "Token requerido")
    try: return jwt.decode(creds.credentials, JWT_SECRET, algorithms=["HS256"])["sub"]
    except jwt.ExpiredSignatureError: raise HTTPException(401, "Sesion expirada")
    except: raise HTTPException(401, "Token invalido")

class Login(BaseModel):
    username: str; password: str

class Product(BaseModel):
    name: str; cat: str; price: float
    sale: Optional[float] = None; stock: int = 0
    sizes: List[str] = []; colors: List[str] = []
    tags: List[str] = []; desc: str = ""
    images: List[str] = []; video: Optional[str] = None
    active: bool = True; offer: Optional[dict] = None

class Order(BaseModel):
    num: str; name: str; phone: str
    email: Optional[str] = None; addr: str; city: str
    dept: str = "Santander"; pay: str; items: List[dict]
    sub: float; ship: float; total: float; status: str = "nuevo"

class Customer(BaseModel):
    name: str; email: Optional[str] = None
    phone: str; city: Optional[str] = None; marketing_ok: bool = True

class StatusUp(BaseModel):
    status: str

@app.get("/")
async def root(): return {"status": "ok", "app": "REYNA MODA API"}

@app.get("/health")
async def health():
    ok = False
    if mongo_client:
        try: await mongo_client.admin.command("ping"); ok = True
        except: pass
    return {"mongo": "conectado" if ok else "sin conexion", "cloudinary": "ok" if CLOUDINARY_CLOUD else "falta config"}

@app.post("/auth/login")
async def login(body: Login):
    exp = ADMIN_USERS.get(body.username)
    if not exp or body.password != exp:
        raise HTTPException(401, "Usuario o contrasena incorrectos")
    return {"access_token": make_token(body.username), "token_type": "bearer", "username": body.username}

@app.post("/upload/image")
async def upload(file: UploadFile = File(...), folder: str = Form("reyna_moda/productos"), _u: str = Depends(auth)):
    if file.content_type not in {"image/jpeg","image/jpg","image/png","image/webp"}:
        raise HTTPException(400, "Usa JPG PNG o WEBP")
    data = await file.read()
    if len(data) > 10*1024*1024: raise HTTPException(400, "Imagen mayor a 10MB")
    try:
        r = cloudinary.uploader.upload(data, folder=folder,
            transformation=[{"width":900,"height":1100,"crop":"fill","gravity":"auto"},
                            {"quality":"auto:good"},{"fetch_format":"auto"}])
        return {"url": r["secure_url"], "public_id": r["public_id"]}
    except Exception as e: raise HTTPException(500, str(e))

@app.delete("/upload/image/{pid:path}")
async def del_img(pid: str, _u: str = Depends(auth)):
    cloudinary.uploader.destroy(pid); return {"deleted": True}

@app.get("/productos")
async def productos(cat: Optional[str] = None):
    q = {"active": True}
    if cat: q["cat"] = cat
    return [sid(p) async for p in db["productos"].find(q).sort("_id", -1)]

@app.get("/productos/admin")
async def productos_admin(_u: str = Depends(auth)):
    return [sid(p) async for p in db["productos"].find({}).sort("_id", -1)]

@app.get("/productos/{pid}")
async def get_prod(pid: str):
    p = await db["productos"].find_one({"_id": ObjectId(pid)})
    if not p: raise HTTPException(404, "No encontrado")
    return sid(p)

@app.post("/productos", status_code=201)
async def create_prod(p: Product, _u: str = Depends(auth)):
    d = p.dict(); d["created_at"] = d["updated_at"] = datetime.utcnow().isoformat()
    r = await db["productos"].insert_one(d); d["_id"] = str(r.inserted_id)
    logger.info(f"Producto creado: {d['name']}"); return d

@app.put("/productos/{pid}")
async def update_prod(pid: str, p: Product, _u: str = Depends(auth)):
    d = p.dict(); d["updated_at"] = datetime.utcnow().isoformat()
    r = await db["productos"].update_one({"_id": ObjectId(pid)}, {"$set": d})
    if r.matched_count == 0: raise HTTPException(404, "No encontrado")
    return {"updated": True}

@app.patch("/productos/{pid}/toggle")
async def toggle_prod(pid: str, _u: str = Depends(auth)):
    p = await db["productos"].find_one({"_id": ObjectId(pid)})
    if not p: raise HTTPException(404, "No encontrado")
    na = not p.get("active", True)
    await db["productos"].update_one({"_id": ObjectId(pid)},
        {"$set": {"active": na, "updated_at": datetime.utcnow().isoformat()}})
    return {"active": na}

@app.delete("/productos/{pid}")
async def del_prod(pid: str, _u: str = Depends(auth)):
    r = await db["productos"].delete_one({"_id": ObjectId(pid)})
    if r.deleted_count == 0: raise HTTPException(404, "No encontrado")
    return {"deleted": True}

@app.get("/pedidos")
async def pedidos(_u: str = Depends(auth)):
    return [sid(o) async for o in db["pedidos"].find({}).sort("_id", -1)]

@app.post("/pedidos", status_code=201)
async def create_pedido(o: Order):
    d = o.dict(); d["created_at"] = datetime.utcnow().isoformat()
    r = await db["pedidos"].insert_one(d); d["_id"] = str(r.inserted_id)
    for it in o.items:
        await db["productos"].update_one({"name": it.get("n")}, {"$inc": {"stock": -it.get("q", 0)}})
    logger.info(f"Pedido: {o.num} ${o.total:,.0f}"); return d

@app.patch("/pedidos/{oid}/status")
async def upd_pedido(oid: str, b: StatusUp, _u: str = Depends(auth)):
    valid = {"nuevo","confirmado","enviado","entregado","cancelado"}
    if b.status not in valid: raise HTTPException(400, f"Estado invalido")
    r = await db["pedidos"].update_one({"_id": ObjectId(oid)}, {"$set": {"status": b.status}})
    if r.matched_count == 0: raise HTTPException(404, "No encontrado")
    return {"updated": True, "status": b.status}

@app.get("/clientes")
async def clientes(_u: str = Depends(auth)):
    return [sid(c) async for c in db["clientes"].find({}).sort("_id", -1)]

@app.post("/clientes", status_code=201)
async def create_cliente(c: Customer):
    q = {"phone": c.phone}
    if c.email: q = {"$or": [{"email": c.email}, {"phone": c.phone}]}
    ex = await db["clientes"].find_one(q)
    if ex:
        await db["clientes"].update_one({"_id": ex["_id"]},
            {"$inc": {"orders": 1}, "$set": {"last_order": datetime.utcnow().isoformat()}})
        return sid(ex)
    d = c.dict()
    d.update({"orders":1,"points":0,"level":"BRONZE",
              "created_at":datetime.utcnow().isoformat(),
              "last_order":datetime.utcnow().isoformat()})
    r = await db["clientes"].insert_one(d); d["_id"] = str(r.inserted_id)
    return d

@app.get("/config")
async def get_config():
    cfg = await db["config"].find_one({"_id": "main"})
    if not cfg:
        return {"paymentMethods":[
            {"id":"nequi","name":"Nequi","detail":"3167470857 Felix Abraham Villamizar","enabled":True},
            {"id":"bancolombia","name":"Transferencia Bancolombia","detail":"Felix Abraham Villamizar","enabled":True},
            {"id":"davivienda","name":"Transferencia Davivienda","detail":"Felix Abraham Villamizar","enabled":True},
            {"id":"contraentrega","name":"Pago Contra Entrega","detail":"Solo area metropolitana","enabled":True},
        ],"shippingZones":[
            {"name":"floridablanca","cost":6000,"desc":"Floridablanca"},
            {"name":"giron","cost":12000,"desc":"Giron"},
            {"name":"piedecuesta","cost":12000,"desc":"Piedecuesta"},
            {"name":"bucaramanga","cost":15000,"desc":"Bucaramanga"},
        ]}
    cfg.pop("_id", None); return cfg

@app.put("/config")
async def upd_config(body: dict, _u: str = Depends(auth)):
    await db["config"].update_one({"_id":"main"}, {"$set":body}, upsert=True)
    return {"updated": True}
