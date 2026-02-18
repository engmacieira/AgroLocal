import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base, GUID

class AuditAction(str, enum.Enum):
    """Padroniza os tipos de eventos rastreados pelo sistema."""
    CREATE = "CREATE"            # Criação de registro
    UPDATE = "UPDATE"            # Atualização de dados
    DELETE = "DELETE"            # Remoção (lógica ou física)
    LOGIN = "LOGIN"              # Acesso ao sistema
    LOGOUT = "LOGOUT"            # Saída
    APPROVE = "APPROVE"          # Curadoria (Admin aprovou produto)
    REJECT = "REJECT"            # Curadoria (Admin rejeitou)
    SYSTEM_EVENT = "SYSTEM_EVENT" # Rotinas automáticas (Ex: Cron jobs)

class AuditLog(Base):
    """
    O 'Gravador de Voo' (Caixa Preta) do sistema.
    Registra alterações críticas para segurança, compliance (LGPD) e resolução de disputas.
    """
    __tablename__ = "audit_logs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Onde ocorreu a mudança?
    table_name = Column(String(50), nullable=False, index=True) # Ex: "producer_products"
    record_id = Column(Integer, nullable=False, index=True)     # ID da linha afetada
    
    # Qual foi a ação?
    action = Column(Enum(AuditAction), nullable=False, index=True) 
    
    # Quem fez a mudança?
    # Nullable=True pois pode ser uma ação do sistema (Cron job) ou usuário anônimo (Login falho)
    actor_id = Column(GUID, ForeignKey("users.id"), nullable=True) 
    
    # Contexto da Requisição (Rastreabilidade Técnica)
    ip_address = Column(String(45), nullable=True) # Suporta IPv4 e IPv6
    user_agent = Column(String(255), nullable=True) # Dispositivo/Navegador usado
    
    # O "Antes" e o "Depois" (O Delta)
    # Ex: old_values={"price": 10.0}, new_values={"price": 12.0}
    old_values = Column(JSON, nullable=True) #
    new_values = Column(JSON, nullable=True) #
    
    # Quando?
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    actor = relationship("User") # Apenas para leitura fácil do responsável