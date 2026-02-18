import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base, GUID

class UserRole(str, enum.Enum):
    """Define os níveis de acesso e responsabilidade no sistema."""
    ADMIN = "ADMIN"          # Acesso total ao painel administrativo
    PRODUTOR = "PRODUTOR"    # Vende produtos
    CLIENTE = "CLIENTE"      # Compra produtos

class User(Base):
    """
    Tabela Mestra de Usuários.
    Centraliza o acesso (Login) e dados comuns a todos os perfis.
    """
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Autenticação e Identificação
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True) # Importante para WhatsApp/Notificações
    avatar_url = Column(String, nullable=True) # Foto de perfil (UX essencial)
    
    # Role e Permissões
    role = Column(Enum(UserRole), default=UserRole.CLIENTE, nullable=False)
    
    # Status e Segurança
    is_active = Column(Boolean, default=True) # Soft delete (nunca deletamos users fisicamente)
    is_verified = Column(Boolean, default=False) # Email verificado?
    terms_accepted_at = Column(DateTime(timezone=True), nullable=True) # Marco legal (LGPD)
    last_login = Column(DateTime(timezone=True), nullable=True) # Auditoria de acesso
    
    # Timestamps de Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # --- Relacionamentos ---

    # 1. Endereços (Um usuário tem N endereços)
    # cascade="all, delete-orphan" garante que se apagar o user, limpa os endereços
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    
    # 2. Perfil de Produtor (1:1 - Apenas se role == PRODUTOR)
    producer_profile = relationship("ProducerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # 3. Histórico de Compras (Como Consumidor)
    # Usamos string no foreign_keys para evitar Import Circular com order_model
    orders_made = relationship(
        "Order",
        foreign_keys="Order.customer_id", 
        back_populates="customer"
    )
    
    # 4. Histórico de Vendas (Como Produtor - Acesso rápido via User, mas ideal ir via ProducerProfile)
    sales_received = relationship(
        "Order",
        foreign_keys="Order.producer_id",
        back_populates="producer"
    )

class ProducerProfile(Base):
    """
    Dados estendidos para quem VENDE (Agricultura Familiar).
    Isolado para não sujar a tabela de usuários com dados bancários/fiscais.
    """
    __tablename__ = "producer_profiles"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(GUID, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Identidade Jurídica/Fiscal (US-01)
    cpf_cnpj = Column(String(20), unique=True, index=True, nullable=False)
    
    # Financeiro (US-07 - Split de Pagamento)
    pix_key = Column(String(100), nullable=False) # Chave para receber repasses
    
    # Vitrine (Marketing da Loja)
    store_name = Column(String(100), index=True, nullable=False) # Ex: "Sitio Dona Benta"
    bio = Column(Text, nullable=True) # História do produtor (gera conexão emocional)
    cover_image = Column(String, nullable=True) # Foto de capa da lojinha
    
    # Reputação (Gamificação futura)
    rating = Column(Float, default=5.0) # Média de estrelas (1.0 a 5.0)
    review_count = Column(Integer, default=0) # Total de avaliações recebidas
    
    # --- Relacionamentos ---
    
    user = relationship("User", back_populates="producer_profile")
    
    # Produtos deste produtor (Aponta para ProducerProduct e não Product genérico)
    products = relationship("ProducerProduct", back_populates="producer")