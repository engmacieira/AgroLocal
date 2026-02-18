import uuid
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base, GUID

class PayoutStatus(str, enum.Enum):
    """Ciclo de vida do repasse ao produtor."""
    SCHEDULED = "SCHEDULED"  # Agendado (ex: D+1, D+15)
    PROCESSING = "PROCESSING" # Enviado ao banco, aguardando confirmação
    PAID = "PAID"            # Dinheiro na conta do produtor (Sucesso)
    FAILED = "FAILED"        # Banco rejeitou (Chave inválida, etc)
    CANCELLED = "CANCELLED"  # Cancelado manualmente (Erro operacional)

class Payout(Base):
    """
    Registro de Saída de Caixa (Outflow).
    Representa a transferência de valores da Plataforma para o Produtor.
    Fundamental para o Livro Caixa e Auditoria Fiscal.
    """
    __tablename__ = "payouts"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Vínculos
    order_id = Column(GUID, ForeignKey("orders.id"), unique=True, nullable=False)
    producer_id = Column(GUID, ForeignKey("producer_profiles.id"), nullable=False)
    
    # Máquina de Estados
    status = Column(Enum(PayoutStatus), default=PayoutStatus.SCHEDULED, index=True)
    
    # --- Valores Monetários (A Matemática do Repasse) ---
    # Guardamos os valores aqui para não depender de recálculos no Order
    amount_gross = Column(Numeric(10, 2), nullable=False) # Valor da Venda (Ex: 100.00)
    amount_fee = Column(Numeric(10, 2), nullable=False)   # Taxa da Plataforma (Ex: 10.00)
    amount_net = Column(Numeric(10, 2), nullable=False)   # Valor Efetivo Transferido (Ex: 90.00)
    
    # --- Dados Bancários (Snapshot) ---
    # Gravamos a chave usada NA HORA DO PAGAMENTO. Se o produtor mudar depois, o histórico fica preservado.
    target_pix_key_snapshot = Column(String(100), nullable=False) 
    
    # --- Execução da Transação ---
    scheduled_for = Column(DateTime(timezone=True), nullable=True) # Data prevista
    processed_at = Column(DateTime(timezone=True), nullable=True)  # Data real da transferência
    
    # Comprovantes e Rastreabilidade
    # bank_transaction_id é o "End-to-End ID" do PIX
    bank_transaction_id = Column(String(100), unique=True, nullable=True, index=True) 
    proof_url = Column(String, nullable=True) # URL do comprovante (PDF/Imagem)
    
    # Auditoria de Erros
    failure_reason = Column(String(255), nullable=True) # Ex: "Chave PIX inexistente"
    notes = Column(Text, nullable=True) # Observações internas do Admin
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    order = relationship("Order", back_populates="payout")
    producer = relationship("ProducerProfile")