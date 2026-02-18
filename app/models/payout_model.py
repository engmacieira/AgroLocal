# Arquivo: app/models/payout_model.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Payout(Base):
    """
    Registra a saída de dinheiro da Plataforma para o Produtor.
    Fundamental para o Livro Caixa da empresa.
    """
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    producer_id = Column(Integer, ForeignKey("producer_profiles.id"), nullable=False)
    
    # Valores
    amount_transferred = Column(Numeric(10, 2), nullable=False) # Valor Líquido (Já descontada a taxa)
    
    # Dados da Transação Bancária (Rastro do Dinheiro)
    source_bank_account = Column(String(100), nullable=True) # Ex: "Nubank - Conta PJ Final 4402"
    target_pix_key = Column(String(100), nullable=False) # Chave usada (Snapshot, caso o produtor mude depois)
    
    transaction_date = Column(DateTime(timezone=True), nullable=False) # Data/Hora real da transferência bancária
    
    # Comprovantes
    proof_url = Column(String, nullable=False) # Upload do comprovante de transferência (PDF/JPG)
    bank_transaction_id = Column(String(100), nullable=True) # ID da transação no extrato bancário (E2E ID do PIX)
    
    notes = Column(Text, nullable=True) # Observações internas do Admin
    
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Quando o registro foi criado no sistema

    # Relacionamentos
    order = relationship("Order", back_populates="payout")
    producer = relationship("ProducerProfile")