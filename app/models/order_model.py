class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    producer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    status = Column(String, default="PENDING") # PENDING, PAID, DELIVERED, CANCELED
    total_amount = Column(Numeric(10, 2), nullable=False)
    
    # 1. Controle de Repasse (Para o Admin saber quem pagar)
    payout_status = Column(String(20), default="PENDING") # PENDING, SCHEDULED, PAID, HELD (Retido)
    
    # 2. Documento Fiscal (Para o Produtor enviar a Nota/Cupom)
    fiscal_document_url = Column(String, nullable=True) # URL do PDF/Imagem da Nota Fiscal
    fiscal_document_number = Column(String(50), nullable=True) # Número da Nota (opcional)
    
    # US-07: Split de Pagamento
    fee_amount = Column(Numeric(10, 2)) # Taxa da plataforma
    net_amount = Column(Numeric(10, 2)) # Valor para o produtor
    
    delivery_type = Column(String) # RETIRADA, DOMICILIO, PONTO_ENCONTRO
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", back_populates="order")
    transaction = relationship("Transaction", back_populates="order", uselist=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Snapshot: Preço e nome na hora da compra (não muda se o produtor mudar o produto depois)
    historical_name = Column(String)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    order = relationship("Order", back_populates="items")