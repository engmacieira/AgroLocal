import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.communication import SubjectType, ParticipantRole, ConversationStatus

class ConversationModel(Base):
    """Tabela Cabeçalho: O Chamado/Tópico da Conversa"""
    __tablename__ = "conversations"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Atores envolvidos
    initiator_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    target_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    
    # Contexto
    subject_type = Column(SQLEnum(SubjectType), nullable=False)
    reference_id = Column(GUID, nullable=True, index=True) # Ex: ID do Pedido
    target_role = Column(SQLEnum(ParticipantRole), nullable=False)
    
    # Máquina de Estados
    status = Column(SQLEnum(ConversationStatus), default=ConversationStatus.OPEN, nullable=False, index=True)
    
    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento 1:N com as Mensagens
    messages = relationship("MessageModel", back_populates="conversation", cascade="all, delete-orphan")

class MessageModel(Base):
    """Tabela Corpo: As mensagens individuais (Imutáveis)"""
    __tablename__ = "messages"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(GUID, ForeignKey("conversations.id"), nullable=False, index=True)
    
    # Autor da Mensagem
    sender_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    sender_role = Column(SQLEnum(ParticipantRole), nullable=False)
    
    # O Texto
    content = Column(Text, nullable=False)
    
    # Timestamp Exato (Para ordenar o Chat)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento Reverso
    conversation = relationship("ConversationModel", back_populates="messages")