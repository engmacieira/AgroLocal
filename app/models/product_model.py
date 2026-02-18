import uuid
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Numeric, Enum, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base, GUID

class AvailabilityType(str, enum.Enum):
    """Define a logística de disponibilidade do item."""
    PRONTA_ENTREGA = "PRONTA_ENTREGA"  # O produto já está colhido/pronto
    ENCOMENDA = "ENCOMENDA"            # O produtor vai colher/produzir após o pedido

class ProducerProduct(Base):
    """
    A Oferta Real (O que vai para o carrinho).
    Representa o vínculo entre um Produtor e um Produto do Catálogo Global.
    Ex: O produtor 'João' vende o item global 'Tomate Carmem' por R$ 5,00/kg.
    """
    __tablename__ = "producer_products"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Vínculos
    producer_id = Column(GUID, ForeignKey("producer_profiles.id"), nullable=False)
    global_product_id = Column(GUID, ForeignKey("global_products.id"), nullable=False)
    
    # Precificação e Unidade
    # Numeric é OBRIGATÓRIO para dinheiro (evita erros de ponto flutuante do Float)
    price = Column(Numeric(10, 2), nullable=False) 
    unit = Column(String(20), default="kg") # Ex: kg, maço, dúzia, bandeja, litro
    
    # Estoque e Disponibilidade
    stock_quantity = Column(Float, default=0.0)
    availability_type = Column(Enum(AvailabilityType), default=AvailabilityType.PRONTA_ENTREGA)
    
    # Regras de Venda (Diferencial para Atacado/Varejo)
    minimum_order_quantity = Column(Float, default=1.0) # Ex: Mínimo 2 kgs
    
    # Informações de Qualidade (O "Frescor" do AgroLocal)
    description = Column(Text, nullable=True) # Ex: "Sem agrotóxicos, colhido na chuva."
    harvest_date = Column(Date, nullable=True) # Data da colheita (Vital para perecíveis)
    
    # Controle
    is_active = Column(Boolean, default=True) # Se false, não aparece na busca
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # --- Relacionamentos ---
    
    # Dados do catálogo geral (Nome, Categoria, Foto padrão)
    global_info = relationship("GlobalProduct", back_populates="offers")
    
    # Quem está vendendo
    producer = relationship("ProducerProfile", back_populates="products")
    
    # Fotos reais deste lote específico (Opcional, mas recomendado para passar confiança)
    images = relationship("ProductImage", back_populates="producer_product", cascade="all, delete-orphan")

class ProductImage(Base):
    """
    Fotos reais do produto ofertado pelo produtor.
    Diferente da foto do catálogo global, essa mostra o estado real do item.
    """
    __tablename__ = "product_images"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    producer_product_id = Column(GUID, ForeignKey("producer_products.id"), nullable=False)
    
    url = Column(String, nullable=False) # URL do S3 / Firebase / MinIO
    is_primary = Column(Boolean, default=False) # Foto de capa da oferta
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    producer_product = relationship("ProducerProduct", back_populates="images")