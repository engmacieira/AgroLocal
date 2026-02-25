import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Text, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base, GUID

class ProducerModel(Base):
    """
    Modelo de Infraestrutura: Perfil do Produtor/Vendedor.
    Tabela isolada para manter os dados financeiros (PIX, Documento) separados do User básico.
    """
    __tablename__ = "producer_profiles"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # unique=True garante a relação 1:1 (Um utilizador = Um perfil de produtor)
    user_id = Column(GUID, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Identidade Jurídica/Fiscal
    document = Column(String(20), unique=True, index=True, nullable=False) # CPF ou CNPJ
    pix_key = Column(String(100), nullable=False)
    
    # Vitrine
    store_name = Column(String(100), index=True, nullable=False)
    bio = Column(Text, nullable=True)
    cover_image = Column(String, nullable=True)
    
    # Reputação
    rating = Column(Float, default=5.0)
    review_count = Column(Integer, default=0)
    
    # Controlo e Auditoria
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())