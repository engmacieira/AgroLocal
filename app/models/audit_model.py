from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class AuditLog(Base):
    """
    O 'Gravador de Voo' (Caixa Preta) do sistema.
    Registra alterações críticas para segurança e resolução de disputas.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Onde ocorreu a mudança?
    table_name = Column(String(50), nullable=False, index=True) # Ex: "producer_products"
    record_id = Column(Integer, nullable=False, index=True)     # ID do registro afetado
    
    # Qual foi a ação?
    action = Column(String(20), nullable=False) # CREATE, UPDATE, DELETE, LOGIN, APPROVE
    
    # Quem fez a mudança?
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Pode ser Null se for o Sistema
    ip_address = Column(String(45), nullable=True) # IPv4 ou IPv6 (Segurança)
    user_agent = Column(String(255), nullable=True) # Navegador/Dispositivo usado
    
    # O "Antes" e o "Depois" (Poderoso!)
    # Usamos JSON para guardar apenas os campos que mudaram
    # Ex: old_values = {"price": 5.00}, new_values = {"price": 2.00}
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento (Opcional, apenas para facilitar queries de quem fez a ação)
    actor = relationship("User")