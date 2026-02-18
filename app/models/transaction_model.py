class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    
    # Identificadores Externos (Vital para auditoria)
    external_transaction_id = Column(String(100), index=True) # ID do PIX/Cartão no Gateway
    payment_method = Column(String(50)) # PIX, CREDIT_CARD
    
    # Valores
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, APPROVED, FAILED, REFUNDED
    
    # Auditoria
    gateway_response = Column(Text, nullable=True) # JSON cru da resposta do gateway (debug)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    order = relationship("Order", back_populates="transaction")