from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.domain.entities.catalog import ProductStatus

# --- Schemas de Categoria ---
class CategoryCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    icon_url: Optional[str] = None

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    icon_url: Optional[str]
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Produto Global ---
class ProductSuggestRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    category_id: UUID
    suggested_by_id: Optional[UUID] = None
    synonyms: Optional[str] = Field(None, max_length=255)
    ncm_code: Optional[str] = Field(None, min_length=8, max_length=8)

class ProductRejectRequest(BaseModel):
    admin_id: UUID # No futuro vira automático pelo Token JWT
    reason: str = Field(..., min_length=5, max_length=255)

class ProductResponse(BaseModel):
    id: UUID
    name: str
    category_id: UUID
    synonyms: Optional[str]
    ncm_code: Optional[str]
    status: ProductStatus
    rejection_reason: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)