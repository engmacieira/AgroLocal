import enum
import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, timezone

class AuditAction(str, enum.Enum):
    """Padroniza os tipos de eventos rastreados pelo sistema."""
    CREATE = "CREATE"            # Criação de registo
    UPDATE = "UPDATE"            # Atualização de dados
    DELETE = "DELETE"            # Remoção
    LOGIN = "LOGIN"              # Acesso ao sistema
    LOGOUT = "LOGOUT"            # Saída
    APPROVE = "APPROVE"          # Curadoria (Admin aprovou)
    REJECT = "REJECT"            # Curadoria (Admin rejeitou)
    SYSTEM_EVENT = "SYSTEM_EVENT" # Rotinas automáticas

@dataclass(kw_only=True)
class AuditLog:
    """
    Entidade de Domínio: A Caixa Preta do sistema.
    Registra alterações e eventos críticos de forma imutável.
    """
    table_name: str
    record_id: str  # Usamos string para suportar tanto UUIDs quanto Integers (se necessário no futuro)
    action: AuditAction
    
    actor_id: Optional[uuid.UUID] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Dicionários flexíveis para guardar o Delta em formato JSON
    old_values: Optional[Dict[str, Any]] = None 
    new_values: Optional[Dict[str, Any]] = None
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Regras de negócio e consistência da auditoria."""
        
        # 1. Validação de Coerência para UPDATE
        if self.action == AuditAction.UPDATE:
            if self.old_values is None or self.new_values is None:
                raise ValueError("Para a ação UPDATE, os campos old_values e new_values são obrigatórios")

        # 2. Higienização de Strings (IP e User Agent)
        if self.ip_address is not None:
            cleaned_ip = str(self.ip_address).strip()
            self.ip_address = cleaned_ip if cleaned_ip else None
            
        if self.user_agent is not None:
            cleaned_ua = str(self.user_agent).strip()
            self.user_agent = cleaned_ua if cleaned_ua else None