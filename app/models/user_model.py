from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    PRODUTOR = "PRODUTOR"
    CLIENTE = "CLIENTE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Define o tipo de usuário conforme solicitado
    role = Column(Enum(UserRole), default=UserRole.CLIENTE, nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False) # Para validação de e-mail/documento
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    # Um usuário pode ter vários endereços (Entrega, Cobrança, Sítio)
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    
    # Perfil específico para Produtores (One-to-One)
    producer_profile = relationship("ProducerProfile", back_populates="user", uselist=False)
    
    # Compras realizadas (Se for Cliente)
    orders_made = relationship("Order", foreign_keys="[Order.customer_id]", back_populates="customer")

class ProducerProfile(Base):
    """
    Dados específicos do vendedor (Produtor Rural).
    Separado para manter a performance da tabela User.
    """
    __tablename__ = "producer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Documentação e Financeiro (US-01 e US-07)
    cpf_cnpj = Column(String(20), unique=True, index=True, nullable=False)
    pix_key = Column(String(100), nullable=False)
    store_name = Column(String(100), index=True) # Nome da "Lojinha" no App
    bio = Column(String(500))
    
    # Reputação
    rating = Column(Float, default=5.0)
    
    # Relacionamentos
    user = relationship("User", back_populates="producer_profile")
    products = relationship("Product", back_populates="owner")
    sales_received = relationship("Order", foreign_keys="[Order.producer_id]", back_populates="producer")