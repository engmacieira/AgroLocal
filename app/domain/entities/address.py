import enum
import uuid
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone

class AddressType(str, enum.Enum):
    """Classifica a finalidade do endereço para a logística."""
    RESIDENCIAL = "RESIDENCIAL"
    COMERCIAL = "COMERCIAL"
    RURAL = "RURAL"
    PONTO_ENCONTRO = "PONTO_ENCONTRO"

@dataclass(kw_only=True)
class Address:
    """
    Entidade de Domínio: Endereço.
    Gerencia as regras de negócio de geolocalização e logística.
    """
    user_id: uuid.UUID
    
    # Dados de Endereçamento Padrão
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
    
    # Dados Opcionais e Logística Rural
    address_type: AddressType = AddressType.RESIDENCIAL
    label: Optional[str] = None
    complement: Optional[str] = None
    reference_point: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Identificadores e Status
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_default: bool = False
    is_active: bool = True
    
    # Auditoria
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    # --- Comportamentos (Regras de Negócio) ---

    def set_as_default(self) -> None:
        """Define este endereço como o principal do usuário."""
        self.is_default = True
        self.updated_at = datetime.now(timezone.utc)

    def remove_default(self) -> None:
        """Remove o status de endereço principal."""
        self.is_default = False
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """Realiza o soft delete do endereço."""
        self.is_active = False
        self.is_default = False # Um endereço inativo não pode ser o padrão
        self.updated_at = datetime.now(timezone.utc)