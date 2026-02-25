import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Text, Numeric, Enum as SQLEnum, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.producer_product import AvailabilityType, DeliveryType

class ProducerProductModel(Base):
    """Modelo de banco de dados para a Oferta do Produtor."""
    __tablename__ = "producer_products"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Chaves Estrangeiras Obrigatórias
    producer_id = Column(GUID, ForeignKey("producer_profiles.id"), nullable=False)
    global_product_id = Column(GUID, ForeignKey("global_products.id"), nullable=False)
    
    # Dinheiro e Unidade (Numeric é vital para precisão financeira)
    price = Column(Numeric(10, 2), nullable=False) 
    unit = Column(String(20), default="kg", nullable=False)
    
    # Logística
    stock_quantity = Column(Float, default=0.0, nullable=False)
    minimum_order_quantity = Column(Float, default=1.0, nullable=False)
    availability_type = Column(SQLEnum(AvailabilityType), default=AvailabilityType.PRONTA_ENTREGA, nullable=False)
    
    # Frescor
    description = Column(Text, nullable=True)
    harvest_date = Column(Date, nullable=True)
    
    # Controle
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    images = relationship("ProductImageModel", back_populates="producer_product", cascade="all, delete-orphan")
    delivery_options = relationship("OfferDeliveryOptionModel", back_populates="producer_product", cascade="all, delete-orphan")

class ProductImageModel(Base):
    """Modelo de banco de dados para as fotos reais do produto."""
    __tablename__ = "product_images"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    producer_product_id = Column(GUID, ForeignKey("producer_products.id"), nullable=False)
    
    url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    producer_product = relationship("ProducerProductModel", back_populates="images")
    
class OfferDeliveryOptionModel(Base):
    """Modelo de banco de dados para as opções logísticas da oferta."""
    __tablename__ = "offer_delivery_options"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    producer_product_id = Column(GUID, ForeignKey("producer_products.id"), nullable=False)
    
    delivery_type = Column(SQLEnum(DeliveryType), nullable=False)
    fee = Column(Numeric(10, 2), default=0.00, nullable=False)
    schedule = Column(String(255), nullable=True)
    is_enabled = Column(Boolean, default=True)

    # Relacionamento
    producer_product = relationship("ProducerProductModel", back_populates="delivery_options")