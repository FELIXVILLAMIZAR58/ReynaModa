"""
backend/app/services/loyalty_service.py

🎁 PROGRAMA DE FIDELIZACIÓN Y PUNTOS

Niveles:
- 🥉 Bronze: 0-499 puntos (0% descuento)
- 🥈 Silver: 500-1499 puntos (5% descuento)
- 🥇 Gold: 1500-4999 puntos (10% descuento)
- 👑 Reyna: 5000+ puntos (15% + envío gratis)

Referidos:
- Comparte link
- Amiga compra → ambas ganan $10,000
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging
import uuid

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────
# MODELOS
# ─────────────────────────────────────────────────────────────────────

class LoyaltyAccount(BaseModel):
    account_id: str
    user_id: str
    total_points: int
    available_points: int
    level: str  # bronze, silver, gold, reyna
    lifetime_spending: float
    total_purchases: int
    referral_code: str
    referrals_made: int
    referral_earnings: float
    created_at: datetime
    updated_at: datetime

class LoyaltyTransaction(BaseModel):
    transaction_id: str
    user_id: str
    type: str  # purchase, referral, redemption, bonus
    points_change: int
    reason: str
    order_id: Optional[str] = None
    created_at: datetime

class ReferralRecord(BaseModel):
    referral_id: str
    referrer_user_id: str
    referred_user_id: str
    referral_code: str
    status: str  # pending, completed, cancelled
    referred_purchase_amount: float
    referrer_reward: float
    referred_reward: float
    created_at: datetime
    completed_at: Optional[datetime] = None

# ─────────────────────────────────────────────────────────────────────
# LOYALTY SERVICE
# ─────────────────────────────────────────────────────────────────────

class LoyaltyService:
    """Servicio de programa de fidelización"""
    
    # Configuración de niveles
    LEVELS = {
        "bronze": {"min": 0, "max": 499, "discount": 0, "free_shipping": False},
        "silver": {"min": 500, "max": 1499, "discount": 5, "free_shipping": False},
        "gold": {"min": 1500, "max": 4999, "discount": 10, "free_shipping": False},
        "reyna": {"min": 5000, "max": 999999, "discount": 15, "free_shipping": True},
    }
    
    # Reglas de puntos
    POINTS_RULES = {
        "purchase": 1,  # 1 peso gastado = 1 punto
        "referral_bonus": 50000,  # 50k en crédito por referir
        "referral_completion": 10000,  # 10k cuando compra amiga
        "birthday": 500,  # Bonus cumpleaños
        "review": 100,  # Por dejar reseña
        "social_share": 50,  # Por compartir en redes
    }
    
    def __init__(self):
        self.transactions: Dict[str, List[LoyaltyTransaction]] = {}
        self.referrals: Dict[str, List[ReferralRecord]] = {}

    async def create_loyalty_account(self, user_id: str) -> LoyaltyAccount:
        """Crear cuenta de fidelización para nuevo usuario"""
        try:
            referral_code = self._generate_referral_code(user_id)
            
            account = LoyaltyAccount(
                account_id=str(uuid.uuid4()),
                user_id=user_id,
                total_points=0,
                available_points=0,
                level="bronze",
                lifetime_spending=0,
                total_purchases=0,
                referral_code=referral_code,
                referrals_made=0,
                referral_earnings=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            logger.info(f"🎁 Cuenta de fidelización creada para {user_id}")
            
            return account
        except Exception as e:
            logger.error(f"Error creating loyalty account: {e}")
            raise

    async def add_points(
        self,
        user_id: str,
        points: int,
        reason: str,
        order_id: Optional[str] = None
    ) -> LoyaltyTransaction:
        """Agregar puntos por diferentes razones"""
        try:
            transaction = LoyaltyTransaction(
                transaction_id=str(uuid.uuid4()),
                user_id=user_id,
                type="purchase",
                points_change=points,
                reason=reason,
                order_id=order_id,
                created_at=datetime.now()
            )
            
            logger.info(f"✅ {points} puntos agregados a {user_id} ({reason})")
            
            return transaction
        except Exception as e:
            logger.error(f"Error adding points: {e}")
            raise

    async def add_referral_bonus(
        self,
        referrer_user_id: str,
        referred_user_id: str,
        referral_code: str
    ) -> Dict[str, Any]:
        """Agregar bonus por referir amiga"""
        try:
            bonus_points = self.POINTS_RULES["referral_bonus"]
            bonus_pesos = 50000  # Equivalente en pesos
            
            referral = ReferralRecord(
                referral_id=str(uuid.uuid4()),
                referrer_user_id=referrer_user_id,
                referred_user_id=referred_user_id,
                referral_code=referral_code,
                status="pending",
                referred_purchase_amount=0,
                referrer_reward=bonus_pesos,
                referred_reward=bonus_pesos,
                created_at=datetime.now()
            )
            
            logger.info(f"🎁 Bonus de referido agregado a {referrer_user_id}")
            
            return {
                "success": True,
                "referral_id": referral.referral_id,
                "referrer_bonus": bonus_pesos,
                "referred_bonus": bonus_pesos,
                "message": "Ambas ganarán $10,000 cuando se complete la compra"
            }
        except Exception as e:
            logger.error(f"Error adding referral bonus: {e}")
            return {"success": False, "error": str(e)}

    async def get_level_by_points(self, total_points: int) -> str:
        """Obtener nivel según puntos"""
        for level_name, config in self.LEVELS.items():
            if config["min"] <= total_points <= config["max"]:
                return level_name
        return "bronze"

    async def apply_discount_by_level(self, user_id: str, purchase_amount: float) -> Dict[str, Any]:
        """Aplicar descuento automático según nivel"""
        try:
            # Obtener nivel del usuario
            # level = await self.get_user_level(user_id)
            level = "gold"  # Mock
            
            config = self.LEVELS.get(level, self.LEVELS["bronze"])
            discount_percent = config["discount"]
            free_shipping = config["free_shipping"]
            
            discount_amount = purchase_amount * (discount_percent / 100)
            final_amount = purchase_amount - discount_amount
            
            logger.info(f"💰 Descuento de {discount_percent}% aplicado a {user_id}")
            
            return {
                "success": True,
                "level": level,
                "original_amount": purchase_amount,
                "discount_percent": discount_percent,
                "discount_amount": discount_amount,
                "final_amount": final_amount,
                "free_shipping": free_shipping
            }
        except Exception as e:
            logger.error(f"Error applying discount: {e}")
            return {"success": False, "error": str(e)}

    async def generate_referral_link(self, user_id: str, referral_code: str) -> str:
        """Generar link de referido único"""
        referral_url = f"https://reynamoda.com/refer/{referral_code}"
        
        logger.info(f"🔗 Link de referido generado para {user_id}")
        
        return referral_url

    async def track_referral(
        self,
        referral_code: str,
        referred_email: str
    ) -> Dict[str, Any]:
        """Rastrear cuando amiga compra con link"""
        try:
            # En producción, buscar referral_code en DB
            
            return {
                "success": True,
                "referral_code": referral_code,
                "referred_email": referred_email,
                "status": "tracked",
                "referrer_reward": 10000,
                "referred_reward": 10000,
                "message": "¡Compra detectada! Bonos agregados a ambas cuentas"
            }
        except Exception as e:
            logger.error(f"Error tracking referral: {e}")
            return {"success": False, "error": str(e)}

    async def redeem_points(
        self,
        user_id: str,
        points_to_redeem: int,
        redemption_type: str = "discount"  # discount, product, credit
    ) -> Dict[str, Any]:
        """Canjear puntos por descuento o producto"""
        try:
            # 100 puntos = $1000 pesos
            peso_value = points_to_redeem * 10
            
            transaction = LoyaltyTransaction(
                transaction_id=str(uuid.uuid4()),
                user_id=user_id,
                type="redemption",
                points_change=-points_to_redeem,
                reason=f"Canje de {points_to_redeem} puntos por {redemption_type}",
                created_at=datetime.now()
            )
            
            logger.info(f"🎁 {points_to_redeem} puntos canjeados por {user_id}")
            
            return {
                "success": True,
                "points_redeemed": points_to_redeem,
                "peso_value": peso_value,
                "redemption_type": redemption_type,
                "message": f"¡Canjeados {points_to_redeem} puntos = ${peso_value:,.0f}!"
            }
        except Exception as e:
            logger.error(f"Error redeeming points: {e}")
            return {"success": False, "error": str(e)}

    async def level_up(
        self,
        user_id: str,
        old_level: str,
        new_level: str
    ) -> Dict[str, Any]:
        """Notificar cuando cliente sube de nivel"""
        try:
            level_emojis = {
                "bronze": "🥉",
                "silver": "🥈",
                "gold": "🥇",
                "reyna": "👑"
            }
            
            new_config = self.LEVELS[new_level]
            
            logger.info(f"{level_emojis[new_level]} {user_id} ascendió a {new_level}")
            
            return {
                "success": True,
                "user_id": user_id,
                "old_level": old_level,
                "new_level": new_level,
                "emoji": level_emojis[new_level],
                "new_discount": new_config["discount"],
                "free_shipping": new_config["free_shipping"],
                "message": f"🎉 ¡Felicidades! Subiste a nivel {new_level.upper()}"
            }
        except Exception as e:
            logger.error(f"Error leveling up: {e}")
            return {"success": False, "error": str(e)}

    async def get_loyalty_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Dashboard completo de fidelización"""
        
        return {
            "user_id": user_id,
            "account": {
                "level": "gold",
                "total_points": 3250,
                "available_points": 3250,
                "points_to_next_level": 1750,
                "lifetime_spending": 250000,
                "total_purchases": 12
            },
            "referral": {
                "referral_code": "REYNA_ABCD1234",
                "referral_link": "https://reynamoda.com/refer/REYNA_ABCD1234",
                "referrals_made": 5,
                "referral_earnings": 50000,
                "pending_referrals": 2
            },
            "level_info": {
                "current": "🥇 Gold",
                "discount": "10%",
                "free_shipping": False,
                "next_level": "👑 Reyna",
                "points_needed": 1750
            },
            "recent_transactions": [
                {
                    "date": "2026-03-14",
                    "type": "purchase",
                    "points": 85000,
                    "description": "Compra de vestido"
                },
                {
                    "date": "2026-03-13",
                    "type": "referral",
                    "points": 10000,
                    "description": "Amiga compró con tu código"
                }
            ]
        }

    def _generate_referral_code(self, user_id: str) -> str:
        """Generar código de referido único"""
        # Formato: REYNA_XXXX
        import random
        import string
        
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        referral_code = f"REYNA_{random_suffix}"
        
        return referral_code

    async def get_leaderboard(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Obtener top referrers (leaderboard)"""
        
        leaderboard = [
            {
                "rank": 1,
                "name": "María García",
                "referrals_made": 25,
                "referral_earnings": 250000,
                "level": "👑 Reyna"
            },
            {
                "rank": 2,
                "name": "Sofía López",
                "referrals_made": 18,
                "referral_earnings": 180000,
                "level": "🥇 Gold"
            },
            {
                "rank": 3,
                "name": "Valentina Ruiz",
                "referrals_made": 12,
                "referral_earnings": 120000,
                "level": "🥇 Gold"
            },
        ]
        
        return leaderboard[:top_n]

    async def get_level_distribution(self) -> Dict[str, int]:
        """Obtener distribución de clientes por nivel"""
        
        return {
            "bronze": 150,
            "silver": 200,
            "gold": 100,
            "reyna": 50
        }

# Instancia global
loyalty_service = LoyaltyService()
