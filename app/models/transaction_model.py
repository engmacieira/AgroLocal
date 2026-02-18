import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base, GUID

class TransactionStatus(str, enum.Enum):
    """Ciclo de vida do pagamento no Gateway."""
    PENDING = "PENDING"      # Aguardando pagamento (PIX gerado)
    APPROVED = "APPROVED"    # Sucesso (Dinheiro garantido)
    FAILED = "FAILED"        # Cartão recusado ou erro
    REFUNDED = "REFUNDED"    # Estornado (Total ou parcial)
    EXPIRED = "EXPIRED"      # PIX não pago no prazo

class PaymentMethod(str, enum.Enum):
    PIX = "PIX"
    CREDIT_CARD = "CREDIT_CARD"

class Transaction(Base):
    """
    Registro da entrada de dinheiro (Inflow).
    Vinculado 1:1 com um Pedido.
    """
    __tablename__ = "transactions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(GUID, ForeignKey("orders.id"), unique=True, nullable=False)
    
    # Configuração do Pagamento
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False) # Valor cobrado
    installments = Column(Integer, default=1) # Parcelas (1 = à vista)
    
    # Status
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, index=True)
    
    # --- Integração com Gateway (Stripe/MercadoPago/Pagar.me) ---
    
    # O ID que o banco/gateway gerou (Nossa prova de vida)
    external_transaction_id = Column(String(100), index=True, nullable=True) 
    
    # Dados para o Frontend exibir o pagamento (Exclusivo PIX)
    pix_qr_code_base64 = Column(Text, nullable=True) # A imagem em base64
    pix_copy_paste = Column(Text, nullable=True) # O código "copia e cola"
    pix_expiration = Column(DateTime(timezone=True), nullable=True) # Até quando vale?
    
    # Auditoria Técnica
    gateway_response = Column(Text, nullable=True) # JSON completo da resposta (Debug)
    failure_reason = Column(String(255), nullable=True) # Ex: "Saldo insuficiente"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    order = relationship("Order", back_populates="transaction")