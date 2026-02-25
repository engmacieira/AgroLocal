import enum
import uuid
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, timezone
from app.domain.entities.producer_product import DeliveryType # Reutilizamos a logística da Oferta!

class OrderStatus(str, enum.Enum):
    """Ciclo de vida do pedido (Simplificado e Otimizado)."""
    CREATED = "CREATED"          # Criado, aguardando pagamento
    PAID = "PAID"                # Pago (Aceite automático pelo produtor)
    PREPARING = "PREPARING"      # Em separação/colheita
    READY = "READY"              # Pronto para retirada/envio
    DELIVERED = "DELIVERED"      # Entregue (Finalizado)
    CANCELED = "CANCELED"        # Cancelado (Exige justificativa)

@dataclass(kw_only=True)
class OrderItem:
    """O registro imutável do item comprado (Snapshot Fiscal)."""
    product_id: uuid.UUID
    product_name_snapshot: str
    unit_snapshot: str
    unit_price_snapshot: Decimal
    quantity: float
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    subtotal: Decimal = field(init=False) # Será calculado automaticamente

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        if self.unit_price_snapshot < Decimal("0.00"):
            raise ValueError("O preço unitário não pode ser negativo")
            
        # Calcula o subtotal garantindo 2 casas decimais para precisão financeira
        self.subtotal = round(self.unit_price_snapshot * Decimal(str(self.quantity)), 2)

@dataclass(kw_only=True)
class Order:
    """A Ordem de Compra de UM produtor (Após o Split do Carrinho)."""
    customer_id: uuid.UUID
    producer_id: uuid.UUID
    delivery_type: DeliveryType
    delivery_fee: Decimal = Decimal("0.00")
    
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    total_amount: Decimal = Decimal("0.00")
    cancellation_reason: Optional[str] = None
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def add_item(self, product_id: uuid.UUID, product_name_snapshot: str, unit_snapshot: str, unit_price_snapshot: Decimal, quantity: float) -> None:
        """Adiciona um item e recalcula imediatamente o total da ordem."""
        item = OrderItem(
            product_id=product_id,
            product_name_snapshot=product_name_snapshot,
            unit_snapshot=unit_snapshot,
            unit_price_snapshot=unit_price_snapshot,
            quantity=quantity
        )
        self.items.append(item)
        self._recalculate_total()
        
    def _recalculate_total(self) -> None:
        """Soma os subtotais dos itens + o frete da modalidade escolhida."""
        subtotal_itens = sum((item.subtotal for item in self.items), Decimal("0.00"))
        self.total_amount = subtotal_itens + self.delivery_fee
        self.updated_at = datetime.now(timezone.utc)

    # --- Máquina de Estados (Transitions) ---

    def mark_as_paid(self) -> None:
        if self.status != OrderStatus.CREATED:
            raise ValueError("Transição de status inválida")
        self.status = OrderStatus.PAID
        self.updated_at = datetime.now(timezone.utc)

    def start_preparing(self) -> None:
        if self.status != OrderStatus.PAID:
            raise ValueError("Transição de status inválida")
        self.status = OrderStatus.PREPARING
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_ready(self) -> None:
        if self.status != OrderStatus.PREPARING:
            raise ValueError("Transição de status inválida")
        self.status = OrderStatus.READY
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_delivered(self) -> None:
        if self.status != OrderStatus.READY:
            raise ValueError("Transição de status inválida")
        self.status = OrderStatus.DELIVERED
        self.updated_at = datetime.now(timezone.utc)

    def cancel(self, reason: str) -> None:
        if not reason or not reason.strip():
            raise ValueError("Justificativa é obrigatória para cancelamento")
        if self.status == OrderStatus.DELIVERED:
            raise ValueError("Não é possível cancelar um pedido já entregue")
            
        self.status = OrderStatus.CANCELED
        self.cancellation_reason = reason.strip()
        self.updated_at = datetime.now(timezone.utc)
        
    def set_delivery_fee(self, fee: Decimal) -> None:
        """Atualiza a taxa de entrega e recalcula o total imediatamente."""
        if fee < Decimal("0.00"):
            raise ValueError("A taxa de entrega não pode ser negativa")
        self.delivery_fee = fee
        self._recalculate_total()