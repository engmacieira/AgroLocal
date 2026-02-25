from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# --- REQUESTS ---

class CreateReviewRequest(BaseModel):
    order_id: UUID
    customer_id: UUID
    rating: int = Field(..., ge=1, le=5, description="Nota de 1 a 5 estrelas")
    comment: Optional[str] = Field(None, max_length=1000, description="Opcional: O que achou dos produtos?")
    photo_url: Optional[str] = Field(None, description="Opcional: URL da foto do produto recebido")

# --- RESPONSES ---

class ReviewResponse(BaseModel):
    id: UUID
    order_id: UUID
    customer_id: UUID
    producer_id: UUID
    rating: int
    comment: Optional[str]
    photo_url: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)