import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.catalog import ProductStatus

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    slug = Column(String(50), unique=True, index=True)
    icon_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

class GlobalProductModel(Base):
    __tablename__ = "global_products"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Dados Básicos e Busca
    name = Column(String(100), unique=True, nullable=False, index=True)
    category_id = Column(GUID, ForeignKey("categories.id"), nullable=False)
    
    scientific_name = Column(String(100), nullable=True)
    synonyms = Column(String(255), nullable=True, index=True) 
    
    # Fiscal e Descritivo
    taxonomy_code = Column(String(50), nullable=True)
    ncm_code = Column(String(8), nullable=True)
    description_template = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    
    # Workflow
    status = Column(SQLEnum(ProductStatus), default=ProductStatus.PENDING, nullable=False)
    suggested_by_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    reviewed_by_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    rejection_reason = Column(String(255), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())