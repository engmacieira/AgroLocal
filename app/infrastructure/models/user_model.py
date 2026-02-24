import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base, GUID # Mantendo a sua importação original
from app.domain.entities.user import UserRole

class UserModel(Base):
    """
    Modelo de Infraestrutura: Usuário.
    Representa EXATAMENTE como os dados são salvos na tabela do banco de dados.
    NÃO contém regras de negócio.
    """
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Mapeando o Enum do domínio para o banco
    role = Column(SQLEnum(UserRole), default=UserRole.CLIENTE, nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    terms_accepted_at = Column(DateTime(timezone=True), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())