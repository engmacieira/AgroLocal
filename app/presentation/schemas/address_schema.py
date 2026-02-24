from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from app.domain.entities.address import AddressType

class AddressCreateRequest(BaseModel):
    """Payload recebido do Frontend para criar um endereço."""
    user_id: UUID # Nota: Mais à frente, tiraremos isto daqui e pegaremos direto do Token JWT logado.
    
    address_type: AddressType = AddressType.RESIDENCIAL
    label: Optional[str] = Field(None, max_length=50)
    
    street: str = Field(..., min_length=2, max_length=150)
    number: str = Field(..., max_length=20)
    complement: Optional[str] = Field(None, max_length=100)
    neighborhood: str = Field(..., min_length=2, max_length=100)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    postal_code: str = Field(..., min_length=8, max_length=9)
    
    reference_point: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AddressUpdateRequest(BaseModel):
    """Payload para atualizar um endereço (campos opcionais)."""
    label: Optional[str] = Field(None, max_length=50)
    street: Optional[str] = Field(None, min_length=2, max_length=150)
    number: Optional[str] = Field(None, max_length=20)
    complement: Optional[str] = Field(None, max_length=100)
    neighborhood: Optional[str] = Field(None, min_length=2, max_length=100)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    postal_code: Optional[str] = Field(None, min_length=8, max_length=9)
    reference_point: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AddressResponse(BaseModel):
    """Payload de resposta enviado ao Frontend."""
    id: UUID
    user_id: UUID
    address_type: AddressType
    label: Optional[str]
    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    postal_code: str
    reference_point: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    is_default: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)