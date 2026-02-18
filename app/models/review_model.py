class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    # Quem avaliou (Consumidor)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Quem foi avaliado (Produtor)
    producer_id = Column(Integer, ForeignKey("producer_profiles.id"), nullable=False)
    # Qual pedido gerou essa avaliação (Garante veracidade)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    
    rating = Column(Integer, nullable=False) # 1 a 5 estrelas
    comment = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    author = relationship("User", foreign_keys=[author_id])
    producer = relationship("ProducerProfile", foreign_keys=[producer_id])
    order = relationship("Order")