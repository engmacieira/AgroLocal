import uuid
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base, GUID

class AddressType(str, enum.Enum):
    """Classifica a finalidade do endereço para a logística."""
    RESIDENCIAL = "RESIDENCIAL"      # Casa do consumidor ou produtor
    COMERCIAL = "COMERCIAL"          # Escritório ou loja
    RURAL = "RURAL"                  # Sítios, Chácaras (Geralmente sem número, vital referência)
    PONTO_ENCONTRO = "PONTO_ENCONTRO" # Para entregas em feiras/praças (US-04)

class Address(Base):
    """
    Endereços para Logística e Geolocalização.
    Suporta tanto endereços urbanos padronizados quanto referências rurais complexas.
    """
    __tablename__ = "addresses"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    
    # Classificação (Vital para separar onde mora de onde entrega)
    address_type = Column(Enum(AddressType), default=AddressType.RESIDENCIAL)
    
    # Identificador amigável (Ex: "Minha Fazenda", "Casa da Mãe", "Banca da Feira")
    label = Column(String(50), nullable=True)
    
    # --- Dados de Endereçamento (Padrão BR) ---
    street = Column(String(150), nullable=False)        
    number = Column(String(20), nullable=False) # String pois pode ser "S/N" ou "Km 12"
    complement = Column(String(100), nullable=True)     
    neighborhood = Column(String(100), nullable=False)  
    city = Column(String(100), nullable=False)          
    state = Column(String(2), nullable=False) # UF (SP, MG, etc)
    postal_code = Column(String(9), nullable=False) # CEP
    
    # --- Logística Rural (O Diferencial do AgroLocal - US-04) ---
    # Em áreas rurais, o ponto de referência vale mais que o nome da rua
    reference_point = Column(String(255), nullable=True) 
    
    # --- Geolocalização (US-05) ---
    # Essencial para o cálculo de distância (Haversine) nas buscas
    latitude = Column(Float, nullable=True) # Futuro: Indexar para PostGIS
    longitude = Column(Float, nullable=True)
    
    # Controle
    is_default = Column(Boolean, default=False) # Endereço principal para cálculo de frete padrão
    is_active = Column(Boolean, default=True) # Soft Delete
    
    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="addresses")