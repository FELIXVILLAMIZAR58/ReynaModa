from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItem(BaseModel):
    productId: str
    productName: str
    price: float
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None

class ShippingInfo(BaseModel):
    address: str
    city: str
    state: str
    zipCode: str
    cost: float = 0.0
    estimatedDays: int = 5

class PaymentInfo(BaseModel):
    method: str  # "nequi", "transfer", "cash_on_delivery"
    status: str  # "pending", "completed", "failed"
    transactionId: Optional[str] = None
    amount: float

class Order(BaseModel):
    id: Optional[str] = None
    userId: str
    items: List[OrderItem]
    shipping: ShippingInfo
    payment: PaymentInfo
    status: str = "pending"  # "pending", "processing", "shipped", "delivered", "cancelled"
    total: float
    notes: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping: ShippingInfo
    paymentMethod: str
    notes: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
