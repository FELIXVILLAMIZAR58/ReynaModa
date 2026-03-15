import logging
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

class ProductService:
    """Servicio de gestión de productos"""
    
    @staticmethod
    async def get_all_products(db, skip: int = 0, limit: int = 20, 
                               category: Optional[str] = None,
                               min_price: Optional[float] = None,
                               max_price: Optional[float] = None,
                               search: Optional[str] = None) -> dict:
        """Obtener todos los productos con filtros"""
        try:
            query = db.collection("products")
            
            # Filtrar por categoría
            if category:
                query = query.where("category", "==", category)
            
            # Filtrar activos
            query = query.where("active", "==", True)
            
            # Ejecutar query
            docs = query.stream()
            products = []
            
            for doc in docs:
                product = doc.to_dict()
                product["id"] = doc.id
                
                # Filtrar por precio
                if min_price and product.get("price", 0) < min_price:
                    continue
                if max_price and product.get("price", 0) > max_price:
                    continue
                
                # Filtrar por búsqueda
                if search:
                    search_lower = search.lower()
                    if search_lower not in product.get("name", "").lower() and \
                       search_lower not in product.get("description", "").lower():
                        continue
                
                products.append(product)
            
            # Paginación
            total = len(products)
            products = products[skip:skip + limit]
            
            return {
                "success": True,
                "data": products,
                "total": total,
                "skip": skip,
                "limit": limit
            }
        
        except Exception as e:
            logger.error(f"Error obteniendo productos: {e}")
            return {"success": False, "error": str(e), "code": 500}
    
    @staticmethod
    async def get_product(db, product_id: str) -> dict:
        """Obtener un producto específico"""
        try:
            doc = db.collection("products").document(product_id).get()
            
            if not doc.exists:
                return {"success": False, "error": "Producto no encontrado", "code": 404}
            
            product = doc.to_dict()
            product["id"] = doc.id
            
            return {"success": True, "data": product}
        
        except Exception as e:
            logger.error(f"Error obteniendo producto: {e}")
            return {"success": False, "error": str(e), "code": 500}
    
    @staticmethod
    async def create_product(db, product_data: dict) -> dict:
        """Crear nuevo producto"""
        try:
            product_doc = {
                "name": product_data["name"],
                "description": product_data["description"],
                "price": product_data["price"],
                "salePrice": product_data.get("salePrice"),
                "category": product_data["category"],
                "sizes": product_data.get("sizes", []),
                "colors": product_data.get("colors", []),
                "stock": product_data["stock"],
                "images": [],
                "video": None,
                "tags": product_data.get("tags", []),
                "rating": 0.0,
                "reviews": 0,
                "active": True,
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            }
            
            # Guardar en Firestore
            doc_ref = db.collection("products").document()
            doc_ref.set(product_doc)
            
            # Crear inventario
            inventory_doc = {
                "productId": doc_ref.id,
                "totalStock": product_data["stock"],
                "available": product_data["stock"],
                "reserved": 0,
                "damaged": 0,
                "lowStockAlert": int(product_data["stock"] * 0.2),
                "reorderLevel": int(product_data["stock"] * 0.3),
                "lastRestocked": datetime.now(timezone.utc),
                "warehouse": "Bucaramanga"
            }
            
            db.collection("inventory").document(doc_ref.id).set(inventory_doc)
            
            return {
                "success": True,
                "data": {"id": doc_ref.id, **product_doc},
                "message": "Producto creado exitosamente"
            }
        
        except Exception as e:
            logger.error(f"Error creando producto: {e}")
            return {"success": False, "error": str(e), "code": 500}
    
    @staticmethod
    async def update_product(db, product_id: str, product_data: dict) -> dict:
        """Actualizar producto"""
        try:
            update_data = {k: v for k, v in product_data.items() if v is not None}
            update_data["updatedAt"] = datetime.now(timezone.utc)
            
            db.collection("products").document(product_id).update(update_data)
            
            return {
                "success": True,
                "message": "Producto actualizado exitosamente"
            }
        
        except Exception as e:
            logger.error(f"Error actualizando producto: {e}")
            return {"success": False, "error": str(e), "code": 500}
    
    @staticmethod
    async def delete_product(db, product_id: str) -> dict:
        """Eliminar producto"""
        try:
            db.collection("products").document(product_id).delete()
            db.collection("inventory").document(product_id).delete()
            
            return {
                "success": True,
                "message": "Producto eliminado exitosamente"
            }
        
        except Exception as e:
            logger.error(f"Error eliminando producto: {e}")
            return {"success": False, "error": str(e), "code": 500}
