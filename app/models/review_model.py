import uuid
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID

class Review(Base):
    """
    Sistema de Reputação.
    Garante a confiança no marketplace através de 'Verified Purchases'.
    Regra: Um pedido = Uma avaliação (1:1).
    """
    __tablename__ = "reviews"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)

    # Atores da Avaliação
    author_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    producer_id = Column(GUID, ForeignKey("producer_profiles.id"), nullable=False)
    
    # O elo de confiança (Só avalia se tiver pedido atrelado)
    order_id = Column(GUID, ForeignKey("orders.id"), unique=True, nullable=False)

    # O Feedback
    rating = Column(Integer, nullable=False) # Escala de 1 a 5
    comment = Column(Text, nullable=True)    # Texto livre

    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Regra de Integridade do Banco (Constraint)
    # Garante que NINGUÉM insira nota 0, -1 ou 10, mesmo se o frontend falhar.
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    # --- Relacionamentos ---
    
    # Apenas referência (Unidirecional por enquanto para não gerar ciclo complexo com User)
    author = relationship("User", foreign_keys=[author_id])
    producer = relationship("ProducerProfile", foreign_keys=[producer_id])
    
    # Bidirecional com Order (Para podermos acessar order.review)
    order = relationship("Order", back_populates="review")