import uuid
from sqlalchemy import Column, Integer, ForeignKey, Text, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID

class ReviewModel(Base):
    """
    Sistema de Reputação no Banco de Dados.
    Garante a confiança no marketplace através de 'Verified Purchases'.
    """
    __tablename__ = "reviews"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)

    # Atores
    customer_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    producer_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    
    # O elo de confiança (1 Pedido = 1 Avaliação)
    order_id = Column(GUID, ForeignKey("orders.id"), unique=True, nullable=False)

    # Feedback
    rating = Column(Integer, nullable=False) 
    comment = Column(Text, nullable=True)    
    photo_url = Column(String(500), nullable=True)

    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # A Última Linha de Defesa do Banco (Constraint)
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    # Relacionamentos
    customer = relationship("UserModel", foreign_keys=[customer_id])
    producer = relationship("UserModel", foreign_keys=[producer_id])
    order = relationship("OrderModel", back_populates="review")