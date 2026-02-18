import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Float, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base, GUID

class OrderStatus(str, enum.Enum):
    """Ciclo de vida do pedido."""
    CREATED = "CREATED"          # Criado, aguardando pagamento
    PAID = "PAID"                # Pago, aguardando aceite do produtor
    CONFIRMED = "CONFIRMED"      # Produtor aceitou (Estoque baixado)
    PREPARING = "PREPARING"      # Em separação/colheita
    READY = "READY"              # Pronto para retirada/envio
    IN_TRANSIT = "IN_TRANSIT"    # Saiu para entrega
    DELIVERED = "DELIVERED"      # Entregue (Finalizado)
    CANCELED = "CANCELED"        # Cancelado (Estorno necessário)
    REFUSED = "REFUSED"          # Produtor recusou (Não tinha estoque)

class DeliveryType(str, enum.Enum):
    """Modalidade de entrega escolhida pelo cliente."""
    RETIRADA = "RETIRADA"              # Vai buscar no sítio
    PONTO_ENCONTRO = "PONTO_ENCONTRO"  # Feira ou praça
    DOMICILIO = "DOMICILIO"            # Delivery tradicional

class Order(Base):
    __tablename__ = "orders"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Atores da Transação (Quem comprou e Quem vendeu)
    # Usamos users.id para manter compatibilidade com o User Model
    customer_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    producer_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    
    # Máquina de Estados
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False, index=True)
    cancellation_reason = Column(Text, nullable=True) # Se cancelado/recusado, por quê?
    
    # Valores Monetários (Use Numeric sempre!)
    total_amount = Column(Numeric(10, 2), nullable=False) # Valor total pago pelo cliente
    
    # Logística
    delivery_type = Column(Enum(DeliveryType), nullable=False)
    delivery_fee = Column(Numeric(10, 2), default=0.00) # Frete (se houver)
    delivery_address_snapshot = Column(Text, nullable=True) # JSON ou texto do endereço no momento da compra (Snapshot)
    
    # --- Financeiro (Split de Pagamento - US-07) ---
    # Esses campos são preenchidos após a confirmação do pagamento
    platform_fee_percentage = Column(Float, default=0.0) # Ex: 10%
    platform_fee_value = Column(Numeric(10, 2), default=0.00) # Ex: R$ 5,00
    producer_net_value = Column(Numeric(10, 2), default=0.00) # Ex: R$ 45,00 (O que vai pro produtor)
    
    # Auditoria e Rastreabilidade
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # --- Relacionamentos ---
    
    # Usamos foreign_keys explicitos para evitar ambiguidade (Cliente vs Produtor)
    customer = relationship("User", foreign_keys=[customer_id], back_populates="orders_made")
    producer = relationship("User", foreign_keys=[producer_id], back_populates="sales_received")
    
    # Itens do pedido (Cascade delete: se apagar pedido, apaga itens. Mas pedido não se apaga, se cancela!)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    # Financeiro (1:1)
    transaction = relationship("Transaction", back_populates="order", uselist=False)
    payout = relationship("Payout", back_populates="order", uselist=False)
    
    # Avaliação (1:1 - O cliente avalia o pedido)
    review = relationship("Review", back_populates="order", uselist=False)

class OrderItem(Base):
    """
    O registro imutável do item comprado.
    Mesmo que o produtor apague o produto depois, este registro deve persistir.
    """
    __tablename__ = "order_items"

    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(GUID, ForeignKey("orders.id"), nullable=False)
    
    # Link com o produto original (pode ficar Null se o produto for deletado fisicamente)
    # Aponta para ProducerProduct (Oferta), não GlobalProduct
    product_id = Column(GUID, ForeignKey("producer_products.id"), nullable=True)
    
    # --- SNAPSHOT (A Verdade Fiscal) ---
    # Copiamos esses dados do produto no momento da compra.
    product_name_snapshot = Column(String(255), nullable=False) # Ex: "Tomate Carmem"
    unit_snapshot = Column(String(20), nullable=False) # Ex: "kg"
    unit_price_snapshot = Column(Numeric(10, 2), nullable=False) # O preço que FOI pago
    
    quantity = Column(Float, nullable=False) # Quantidade comprada
    subtotal = Column(Numeric(10, 2), nullable=False) # Qtd * Preço (Facilita queries de relatório)
    
    # Relacionamentos
    order = relationship("Order", back_populates="items")
    product = relationship("ProducerProduct") # Apenas para consulta, se ainda existir