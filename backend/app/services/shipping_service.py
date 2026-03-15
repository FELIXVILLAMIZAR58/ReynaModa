from app.config import LOCAL_SHIPPING_CITIES, LOCAL_SHIPPING_COST, NATIONAL_SHIPPING_BASE
import logging

logger = logging.getLogger(__name__)

class ShippingService:
    """Servicio de cálculo de envíos"""
    
    @staticmethod
    def calculate_shipping(city: str, weight_kg: float = 1.0) -> dict:
        """Calcular costo de envío"""
        try:
            if city in LOCAL_SHIPPING_CITIES:
                # Envío local económico
                cost = LOCAL_SHIPPING_COST
                days = 2
            else:
                # Envío nacional
                # Base + costo por peso
                cost = NATIONAL_SHIPPING_BASE + (weight_kg * 2)
                days = 5
            
            return {
                "success": True,
                "cost": cost,
                "estimatedDays": days,
                "city": city,
                "isLocal": city in LOCAL_SHIPPING_CITIES
            }
        
        except Exception as e:
            logger.error(f"Error calculando envío: {e}")
            return {"success": False, "error": str(e), "code": 500}
    
    @staticmethod
    def get_local_cities() -> list:
        """Obtener ciudades de envío local"""
        return LOCAL_SHIPPING_CITIES
    
    @staticmethod
    def get_all_cities() -> list:
        """Obtener todas las ciudades principales de Colombia"""
        return [
            # Departamento de Santander
            "Bucaramanga", "Floridablanca", "Girón", "Piedecuesta",
            # Principales ciudades
            "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
            "Santa Marta", "Cúcuta", "Buenaventura", "Pereira", "Manizales",
            "Armenia", "Ibagué", "Villavicencio", "Montería", "Valledupar",
            "Riohacha", "Tunja", "Popayán", "Pasto", "Quibdó", "Leticia"
        ]
