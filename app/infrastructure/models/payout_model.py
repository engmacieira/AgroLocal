import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.payout import PayoutStatus

class PayoutModel(Base):
    __tablename__ = "payouts"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Vínculos
    order_id = Column(GUID, ForeignKey("orders.id"), unique=True, nullable=False)
    producer_id = Column(GUID, ForeignKey("users.id"), nullable=False) # O produtor é um User
    
    # Máquina de Estados
    status = Column(SQLEnum(PayoutStatus), default=PayoutStatus.SCHEDULED, index=True)
    
    # Valores Monetários
    amount_gross = Column(Numeric(10, 2), nullable=False)
    amount_fee = Column(Numeric(10, 2), nullable=False)
    amount_net = Column(Numeric(10, 2), nullable=False)
    
    # Dados Bancários (Snapshot)
    target_pix_key_snapshot = Column(String(100), nullable=False) 
    
    # Execução
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Comprovativos
    bank_transaction_id = Column(String(100), unique=True, nullable=True, index=True) 
    proof_url = Column(String, nullable=True)
    
    # Auditoria
    failure_reason = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    order = relationship("OrderModel", back_populates="payout")