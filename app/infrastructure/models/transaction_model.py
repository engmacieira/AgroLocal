import uuid
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.transaction import TransactionStatus, PaymentMethod

class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Configuração do Pagamento
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    installments = Column(Integer, default=1)
    
    # Status
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING, index=True)
    
    # Integração
    external_transaction_id = Column(String(100), index=True, nullable=True) 
    failure_reason = Column(String(255), nullable=True)
    
    # Dados do PIX
    pix_qr_code_base64 = Column(Text, nullable=True)
    pix_copy_paste = Column(Text, nullable=True)
    pix_expiration = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento 1:N (Uma Transação para Vários Pedidos)
    orders = relationship("OrderModel", back_populates="transaction")