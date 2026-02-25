from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID

class ProducerCreateRequest(BaseModel):
    """Payload para transformar um utilizador num produtor."""
    user_id: UUID
    store_name: str = Field(..., min_length=2, max_length=100)
    document: str = Field(..., min_length=11, max_length=20) # Acomoda CPF (11) ou CNPJ (14)
    pix_key: str = Field(..., min_length=5, max_length=100)
    bio: Optional[str] = None
    cover_image: Optional[str] = None

class ProducerUpdateRequest(BaseModel):
    """Payload para atualizar dados da loja (todos opcionais)."""
    store_name: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = None
    pix_key: Optional[str] = Field(None, min_length=5, max_length=100)

class ProducerResponse(BaseModel):
    """Payload de resposta com os dados públicos do produtor."""
    id: UUID
    user_id: UUID
    store_name: str
    document: str
    pix_key: str
    bio: Optional[str]
    cover_image: Optional[str]
    rating: float
    review_count: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)