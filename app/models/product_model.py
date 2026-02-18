class ProducerProduct(Base):
    """A oferta específica de um produtor vinculado a um item global."""
    __tablename__ = "producer_products"

    id = Column(Integer, primary_key=True, index=True)
    producer_id = Column(Integer, ForeignKey("producer_profiles.id"), nullable=False)
    global_product_id = Column(Integer, ForeignKey("global_products.id"), nullable=False)
    
    # Especificidades da oferta do produtor
    price = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20), default="kg") # maço, unidade, kg
    stock_quantity = Column(Float, default=0.0)
    
    # US-03: Flexibilidade de Entrega
    availability_type = Column(String, default="PRONTA_ENTREGA") # ou ENCOMENDA
    description = Column(Text) # Detalhes do produtor (ex: "Colhido hoje cedo")
    
    is_active = Column(Boolean, default=True)

    # Relacionamentos
    global_info = relationship("GlobalProduct", back_populates="offers")
    producer = relationship("ProducerProfile", back_populates="products")
    images = relationship("ProductImage", back_populates="producer_product")

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True)
    # Vínculo direto com a oferta do produtor, não com o produto global
    producer_product_id = Column(Integer, ForeignKey("producer_products.id"), nullable=False)
    
    url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False) # A foto de capa da oferta
    
    # Relacionamento
    producer_product = relationship("ProducerProduct", back_populates="images")