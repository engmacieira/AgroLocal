import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base, GUID

class ProductStatus(str, enum.Enum):
    """Workflow de aprovação de novos itens no catálogo."""
    PENDING = "PENDING"      # Aguardando análise do Admin
    APPROVED = "APPROVED"    # Visível para todos os produtores usarem
    REJECTED = "REJECTED"    # Recusado (ver motivo)
    ARCHIVED = "ARCHIVED"    # Saiu de linha / Sazonalidade inativa

class Category(Base):
    """
    Categorias dos produtos (Ex: Frutas, Legumes, Laticínios).
    Fundamental para a navegação no App (US-05).
    """
    __tablename__ = "categories"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    slug = Column(String(50), unique=True, index=True) # Para URL amigável (ex: /categoria/frutas-citricas)
    icon_url = Column(String, nullable=True) # Ícone para o App
    is_active = Column(Boolean, default=True)
    
    # Relacionamento
    products = relationship("GlobalProduct", back_populates="category")

class GlobalProduct(Base):
    """
    Catálogo Mestre (A "Verdade" sobre o produto).
    Evita duplicidade. O produtor vincula sua oferta a este registro.
    """
    __tablename__ = "global_products"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Dados Básicos
    name = Column(String(100), unique=True, nullable=False, index=True)
    scientific_name = Column(String(100), nullable=True) # Ex: Manihot esculenta
    
    # Busca Inteligente (O "Pulo do Gato" para regionalismos)
    # Ex: "aipim, macaxeira, castelinha"
    synonyms = Column(String(255), nullable=True, index=True) 
    
    # Classificação
    category_id = Column(GUID, ForeignKey("categories.id"), nullable=False)
    
    # Fiscal e Descritivo
    taxonomy_code = Column(String(50), nullable=True) # Código interno de taxonomia
    ncm_code = Column(String(8), nullable=True) # NCM (8 dígitos) para Nota Fiscal
    description_template = Column(Text) # Descrição base para ajudar o produtor
    image_url = Column(String, nullable=True) # Foto de referência ("Boneco")
    
    # --- Moderação e Curadoria ---
    status = Column(Enum(ProductStatus), default=ProductStatus.PENDING, nullable=False)
    
    # Quem sugeriu? (Se null, foi o próprio Admin)
    suggested_by_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    
    # Quem aprovou/rejeitou?
    reviewed_by_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    rejection_reason = Column(String(255), nullable=True) # Feedback para o produtor
    
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- Relacionamentos ---
    
    category = relationship("Category", back_populates="products")
    
    # Ofertas dos produtores vinculadas a este item global
    offers = relationship("ProducerProduct", back_populates="global_info")
    
    # Rastreabilidade de quem sugeriu/aprovou
    suggester = relationship("User", foreign_keys=[suggested_by_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by_id])