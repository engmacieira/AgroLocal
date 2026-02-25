import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.audit import AuditAction

class AuditModel(Base):
    """
    O 'Gravador de Voo' (Caixa Preta) do banco de dados.
    """
    __tablename__ = "audit_logs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Onde ocorreu a mudança?
    table_name = Column(String(50), nullable=False, index=True)
    record_id = Column(String(255), nullable=False, index=True) # String para suportar UUIDs e Integers
    
    # Qual foi a ação?
    action = Column(SQLEnum(AuditAction), nullable=False, index=True) 
    
    # Quem fez a mudança?
    actor_id = Column(GUID, ForeignKey("users.id"), nullable=True) 
    
    # Contexto
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    # O "Antes" e o "Depois" (Deltas JSON)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    
    # Timestamp Imutável
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relacionamento de Leitura
    actor = relationship("UserModel")