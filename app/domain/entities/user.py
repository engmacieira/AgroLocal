import enum
import uuid
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    PRODUTOR = "PRODUTOR"
    CLIENTE = "CLIENTE"

@dataclass(kw_only=True)
class User:
    """
    Entidade de Domínio: Usuário.
    """
    email: str
    password_hash: str
    full_name: str
    role: UserRole = UserRole.CLIENTE
    
    # Dados opcionais (podem ser preenchidos depois)
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    
    # Identificadores e Status padrão
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True
    is_verified: bool = False
    
    # Datas de Auditoria e Marcos
    terms_accepted_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    # --- Comportamentos (Regras de Negócio) ---

    def accept_terms(self) -> None:
        """Registra o aceite dos termos de uso (LGPD)."""
        self.terms_accepted_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def verify_account(self) -> None:
        """Marca a conta como verificada (ex: após clique no link de email)."""
        self.is_verified = True
        self.updated_at = datetime.now(timezone.utc)

    def register_login(self) -> None:
        """Atualiza a data do último login realizado."""
        self.last_login = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """Realiza o soft delete do usuário."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)