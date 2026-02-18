from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Identificador amigável (Ex: "Minha Fazenda", "Casa", "Ponto da Feira")
    label = Column(String(50), nullable=True)
    
    # Padrão Brasileiro de Endereçamento
    street = Column(String(150), nullable=False)        # Rua / Logradouro
    number = Column(String(20), nullable=False)         # Número (String para suportar "S/N")
    complement = Column(String(100), nullable=True)     # Complemento (Apt, Bloco, Km)
    neighborhood = Column(String(100), nullable=False)  # Bairro
    city = Column(String(100), nullable=False)          # Cidade
    state = Column(String(2), nullable=False)           # Estado (UF: SP, MG, etc)
    postal_code = Column(String(9), nullable=False)     # CEP (00000-000)
    
    # Vital para logística rural e entregas (US-04)
    reference_point = Column(String(255), nullable=True) # Ponto de referência
    
    # Geolocalização para busca por proximidade (US-05)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Controle de entrega
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relacionamento inverso
    user = relationship("User", back_populates="addresses")