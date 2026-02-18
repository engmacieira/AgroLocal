class GlobalProduct(Base):
    """Catálogo oficial da plataforma. Controlado pelo Admin."""
    __tablename__ = "global_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Taxonomia e NCM (Nomenclatura Comum do Mercosul) para fins fiscais futuros
    taxonomy_code = Column(String(50), nullable=True) 
    description_template = Column(Text) # Sugestão de descrição para o produtor
    
    # Status de Curadoria
    is_approved = Column(Boolean, default=False) # Para sua sugestão de aprovação
    suggested_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    category = relationship("Category", back_populates="products")
    offers = relationship("ProducerProduct", back_populates="global_info")