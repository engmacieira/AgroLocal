from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import enum
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from app.domain.entities.order import OrderStatus
from app.domain.entities.producer_product import DeliveryType

# --- REQUEST SCHEMAS (O Carrinho que vem do Frontend) ---

class CheckoutItemRequest(BaseModel):
    offer_id: UUID
    quantity: float = Field(..., gt=0) # Garante que ninguém compra "0" ou "-1" itens

class CheckoutProducerGroupRequest(BaseModel):
    producer_id: UUID
    delivery_type: DeliveryType
    items: List[CheckoutItemRequest]

class CheckoutCartRequest(BaseModel):
    customer_id: UUID
    groups: List[CheckoutProducerGroupRequest]

# --- RESPONSE SCHEMAS (O Pedido gerado que devolvemos) ---

class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    product_name_snapshot: str
    unit_snapshot: str
    unit_price_snapshot: Decimal
    quantity: float
    subtotal: Decimal
    
    model_config = ConfigDict(from_attributes=True)

class OrderAction(str, enum.Enum):
    """Ações permitidas para mudar o status do pedido."""
    PAID = "PAID"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"

class OrderStatusUpdateRequest(BaseModel):
    """Payload para a mudança de estado."""
    action: OrderAction
    reason: Optional[str] = Field(None, description="Obrigatório caso a ação seja CANCELED")

class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    producer_id: UUID
    delivery_type: DeliveryType
    delivery_fee: Decimal
    status: OrderStatus
    total_amount: Decimal
    cancellation_reason: Optional[str]
    created_at: datetime
    items: List[OrderItemResponse]
    
    model_config = ConfigDict(from_attributes=True)