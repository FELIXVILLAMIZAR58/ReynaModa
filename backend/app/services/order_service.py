import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class OrderService:
    """Servicio de gestión de órdenes"""
    
    @staticmethod
    async def create_order(db, user_id: str, order_data: dict) -> dict:
        """Crear nueva orden"""
        try:
            # Calcular total
            subtotal = sum(item["price"] * item["quantity"] for item in order_data["items"])
            total = subtotal + order_data["shipping"].get("cost", 0)
            
            order_doc = {
                "userId": user_id,
                "items": order_data["items"],
                "shipping": order_data["shipping"],
                "payment": {
                    "method": order_data["paymentMethod"],
                    "status": "pending",
                    "transactionId": None,
                    "amount": total
                },
                "status": "pending",
                "total": total,
                "notes": order_data.get("notes"),
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            }
            
            # Guardar orden
            doc_ref = db.collection("orders").document()
            doc_ref.set(order_doc)
            
            # Actualizar inventario
            for item in order_data["items"]:
                inventory_ref = db.collection("inventory").document(item["productId"])
                inventory_doc = inventory_ref.get()
                
                if inventory_doc.exists:
                    inventory_data = inventory_doc.to_dict()
                    inventory_ref.update({
                        "available": inventory_data["available"] - item["quantity"],
                        "reserved": inventory_data.get("reserved", 0) + item["quantity"]
                    })
            
            # Agregar orden al perfil del usuario
            db.collection("users").document(user_id).update({
                "orders": db.collection("users").document(user_id).get().to_dict().get("orders", []) + [doc_ref.id]
            })
            
            return {
                "success": True,
                "data": {"id": doc_ref.id, **order_doc},
                "message": "Orden creada exitosamente"
            }
        
        except Exception as e:
            logger.error(f"Error creando orden: {e}")
            return {"success": False, "error": str(e), "code": 500}
    
    @staticmethod
    async def get_user_orders(db, user_id: str, skip: int = 0, limit: int = 20) -> dict:
        """Obtener órdenes del usuario"""
        try:
            query = db.collection("orders").where("userId", "==", user_id)
            docs = list(query.stream())
            
            orders = []
            for doc in docs:
                order = doc.to_dict()
                order["id"] = doc.id
                orders.append(order)
            
            # Ordenar por fecha descendente
            orders.sort(key=lambda x: x.get("createdAt", datetime.now(timezone.utc)), reverse=True)
            
            # Paginación
            total = len(orders)
            orders = orders[skip:skip + limit]
            
            return {
                "success": True,
                "data": orders,
                "total": total
            }
        
        except Exception as e:
            logger.error(f"Error obteniendo órdenes: {e}")
            return {"success": False, "error": str(e), "code": 500}
    
    @staticmethod
    async def get_all_orders(db, skip: int = 0, limit: int = 20) -> dict:
        """Obtener todas las órdenes (admin)"""
        try:
            docs = list(db.collection("orders").stream())
            
            orders = []
            for doc in docs:
                order = doc.to_dict()
                order["id"] = doc.id
                orders.append(order)
            
            # Ordenar por fecha descendente
            orders.sort(key=lambda x: x.get("createdAt", datetime.now(timezone.utc)), reverse=True)
            
            # Paginación
            total = len(orders)
            orders = orders[skip:skip + limit]
            
            return {
                "success": True,
                "data": orders,
                "total": total
            }
        
        except Exception as e:
            logger.error(f"Error obteniendo órdenes: {e}")
            return {"success": False, "error": str(e), "code": 500}
    
    @staticmethod
    async def update_order_status(db, order_id: str, status: str, notes: str = None) -> dict:
        """Actualizar estado de orden"""
        try:
            update_data = {
                "status": status,
                "updatedAt": datetime.now(timezone.utc)
            }
            
            if notes:
                update_data["notes"] = notes
            
            db.collection("orders").document(order_id).update(update_data)
            
            return {
                "success": True,
                "message": f"Orden actualizada a {status}"
            }
        
        except Exception as e:
            logger.error(f"Error actualizando orden: {e}")
            return {"success": False, "error": str(e), "code": 500}
