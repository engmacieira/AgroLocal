from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import date
from app.domain.entities.producer_product import AvailabilityType, DeliveryType

class OfferCreateRequest(BaseModel):
    """Payload recebido para criar uma nova oferta."""
    producer_id: UUID
    global_product_id: UUID
    price: Decimal = Field(..., gt=0) # gt=0 garante que o preço seja Greater Than (Maior que) zero
    unit: str = Field(default="kg", max_length=20)
    stock_quantity: float = Field(default=0.0, ge=0.0) # ge=0.0 (Maior ou igual a zero)
    minimum_order_quantity: float = Field(default=1.0, gt=0.0)
    availability_type: AvailabilityType = AvailabilityType.PRONTA_ENTREGA
    description: Optional[str] = None
    harvest_date: Optional[date] = None

class OfferStockUpdateRequest(BaseModel):
    """Payload para adicionar/remover estoque."""
    add_quantity: float # Pode ser negativo para subtrair

class OfferUpdateRequest(BaseModel):
    """Payload para alterar preço ou descrição."""
    new_price: Optional[Decimal] = Field(None, gt=0)
    new_description: Optional[str] = None

class ProductImageResponse(BaseModel):
    id: UUID
    url: str
    is_primary: bool
    model_config = ConfigDict(from_attributes=True)
    
class DeliveryOptionRequest(BaseModel):
    delivery_type: DeliveryType
    fee: Decimal = Field(default=0.0, ge=0) # ge=0 garante taxa não negativa
    schedule: Optional[str] = Field(None, max_length=100)
    is_enabled: bool = True

class DeliveryOptionsUpdateRequest(BaseModel):
    options: List[DeliveryOptionRequest]

class OfferImageAddRequest(BaseModel):
    url: str = Field(..., min_length=5)
    is_primary: bool = False

class DeliveryOptionResponse(BaseModel):
    id: UUID
    delivery_type: DeliveryType
    fee: Decimal
    schedule: Optional[str]
    is_enabled: bool
    model_config = ConfigDict(from_attributes=True)

class OfferResponse(BaseModel):
    """Payload de resposta devolvido pela API."""
    id: UUID
    producer_id: UUID
    global_product_id: UUID
    price: Decimal
    unit: str
    stock_quantity: float
    minimum_order_quantity: float
    availability_type: AvailabilityType
    description: Optional[str]
    harvest_date: Optional[date]
    is_active: bool
    images: List[ProductImageResponse] = []
    delivery_options: List[DeliveryOptionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)