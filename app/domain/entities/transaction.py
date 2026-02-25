import enum
import uuid
from decimal import Decimal
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timezone
from app.domain.entities.order import Order

class TransactionStatus(str, enum.Enum):
    """Ciclo de vida do pagamento no Gateway."""
    PENDING = "PENDING"      # Aguardando pagamento (PIX gerado)
    APPROVED = "APPROVED"    # Sucesso (Dinheiro garantido)
    FAILED = "FAILED"        # Cartão recusado ou erro
    REFUNDED = "REFUNDED"    # Estornado (Total ou parcial)
    EXPIRED = "EXPIRED"      # PIX não pago no prazo

class PaymentMethod(str, enum.Enum):
    PIX = "PIX"
    CREDIT_CARD = "CREDIT_CARD"

@dataclass(kw_only=True)
class Transaction:
    """
    Registro da entrada de dinheiro (Inflow).
    Um pagamento único que quita um ou mais Pedidos do carrinho.
    """
    payment_method: PaymentMethod
    orders: List[Order]
    installments: int = 1
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: TransactionStatus = TransactionStatus.PENDING
    amount: Decimal = field(init=False) # Será calculado automaticamente
    
    # Integração
    external_transaction_id: Optional[str] = None
    failure_reason: Optional[str] = None
    
    # Dados do PIX (Opcionais)
    pix_qr_code_base64: Optional[str] = None
    pix_copy_paste: Optional[str] = None
    pix_expiration: Optional[datetime] = None
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Regras de negócio imediatas na criação."""
        if not self.orders:
            raise ValueError("Uma transação deve conter pelo menos um pedido")
            
        # Calcula o valor total somando todos os pedidos do carrinho
        total = sum((pedido.total_amount for pedido in self.orders), Decimal("0.00"))
        
        if total <= Decimal("0.00"):
            raise ValueError("O valor da transação deve ser maior que zero")
            
        self.amount = total

    # --- Comportamentos (Máquina de Estados Financeira) ---

    def approve(self, external_id: str) -> None:
        """Aprova o pagamento e propaga a aprovação para todos os pedidos."""
        if self.status != TransactionStatus.PENDING:
            raise ValueError("Apenas transações pendentes podem ser aprovadas")
            
        self.status = TransactionStatus.APPROVED
        self.external_transaction_id = external_id
        self.updated_at = datetime.now(timezone.utc)
        
        # Cascata: Se o pagamento passou, todos os pedidos estão pagos!
        for pedido in self.orders:
            pedido.mark_as_paid()

    def fail(self, reason: str) -> None:
        """Registra a falha do pagamento (Cartão recusado, etc)."""
        if self.status != TransactionStatus.PENDING:
            raise ValueError("Apenas transações pendentes podem falhar")
            
        self.status = TransactionStatus.FAILED
        self.failure_reason = reason
        self.updated_at = datetime.now(timezone.utc)

    def expire(self) -> None:
        """Expira o pagamento (Ex: PIX não foi pago dentro do tempo limite)."""
        if self.status != TransactionStatus.PENDING:
            raise ValueError("Apenas transações pendentes podem expirar")
            
        self.status = TransactionStatus.EXPIRED
        self.updated_at = datetime.now(timezone.utc)