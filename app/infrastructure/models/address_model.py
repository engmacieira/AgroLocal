import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.address import AddressType

class AddressModel(Base):
    """
    Modelo de Infraestrutura: Endereço.
    Representa a tabela na base de dados, sem regras de negócio.
    """
    __tablename__ = "addresses"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    
    address_type = Column(SQLEnum(AddressType), default=AddressType.RESIDENCIAL)
    label = Column(String(50), nullable=True)
    
    # Dados de Endereçamento
    street = Column(String(150), nullable=False)        
    number = Column(String(20), nullable=False)
    complement = Column(String(100), nullable=True)     
    neighborhood = Column(String(100), nullable=False)  
    city = Column(String(100), nullable=False)          
    state = Column(String(2), nullable=False)
    postal_code = Column(String(9), nullable=False)
    
    # Logística Rural / Geolocalização
    reference_point = Column(String(255), nullable=True) 
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Controlo
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())