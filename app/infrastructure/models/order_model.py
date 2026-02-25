import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric, Float, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.order import OrderStatus
from app.domain.entities.producer_product import DeliveryType

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Atores da Transação
    customer_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    producer_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    
    # Máquina de Estados
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.CREATED, nullable=False, index=True)
    cancellation_reason = Column(Text, nullable=True) 
    
    # Valores Monetários e Logística
    total_amount = Column(Numeric(10, 2), nullable=False) 
    delivery_type = Column(SQLEnum(DeliveryType), nullable=False)
    delivery_fee = Column(Numeric(10, 2), default=0.00) 
    
    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    transaction_id = Column(GUID, ForeignKey("transactions.id"), nullable=True, index=True)
    transaction = relationship("TransactionModel", back_populates="orders")
    
    # Usamos cascade delete-orphan para garantir que os itens vão junto com o pedido
    items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")
    payout = relationship("PayoutModel", back_populates="order", uselist=False, cascade="all, delete-orphan")

class OrderItemModel(Base):
    """O registro imutável do item comprado (A Verdade Fiscal)."""
    __tablename__ = "order_items"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(GUID, ForeignKey("orders.id"), nullable=False)
    
    # Link com a oferta original (Null se a oferta for deletada no futuro)
    product_id = Column(GUID, ForeignKey("producer_products.id"), nullable=True)
    
    # SNAPSHOT
    product_name_snapshot = Column(String(255), nullable=False)
    unit_snapshot = Column(String(20), nullable=False)
    unit_price_snapshot = Column(Numeric(10, 2), nullable=False)
    
    quantity = Column(Float, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    # Relacionamento
    order = relationship("OrderModel", back_populates="items")