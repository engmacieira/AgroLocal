import enum
import uuid
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone

class PayoutStatus(str, enum.Enum):
    """Ciclo de vida do repasse ao produtor."""
    SCHEDULED = "SCHEDULED"  # Agendado para pagamento
    PROCESSING = "PROCESSING" # Sendo enviado ao banco
    PAID = "PAID"            # Dinheiro na conta do produtor
    FAILED = "FAILED"        # Banco rejeitou (Ex: Chave PIX errada)
    CANCELLED = "CANCELLED"  # Cancelado manualmente

@dataclass(kw_only=True)
class Payout:
    """
    Entidade: Registro de Saída de Caixa (Outflow).
    Garante a correta divisão do dinheiro entre a Plataforma e o Produtor.
    """
    order_id: uuid.UUID
    producer_id: uuid.UUID
    target_pix_key_snapshot: str
    
    amount_gross: Decimal # Valor total da venda
    amount_fee: Decimal   # Taxa retida pela plataforma (AgroLocal)
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: PayoutStatus = PayoutStatus.SCHEDULED
    amount_net: Decimal = field(init=False) # Valor que o produtor efetivamente recebe
    
    scheduled_for: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    bank_transaction_id: Optional[str] = None
    proof_url: Optional[str] = None
    failure_reason: Optional[str] = None
    notes: Optional[str] = None
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Regras financeiras estritas no momento da criação."""
        if self.amount_fee > self.amount_gross:
            raise ValueError("A taxa da plataforma não pode ser maior que o valor bruto")
        if self.amount_fee < Decimal("0.00") or self.amount_gross <= Decimal("0.00"):
            raise ValueError("Valores financeiros inválidos (negativos ou zero)")
            
        # Calcula o líquido (Net) de forma segura
        self.amount_net = self.amount_gross - self.amount_fee
        
        # Agenda imediatamente (Ex: Para hoje mesmo, mas numa app real poderia ser D+1, D+15)
        if not self.scheduled_for:
            self.scheduled_for = datetime.now(timezone.utc)

    # --- Comportamentos ---

    def mark_as_paid(self, bank_transaction_id: str, proof_url: str) -> None:
        """Confirma a transferência do dinheiro para o produtor."""
        if not bank_transaction_id or not proof_url:
            raise ValueError("ID bancário e comprovante são obrigatórios para marcar como pago")
            
        self.status = PayoutStatus.PAID
        self.bank_transaction_id = bank_transaction_id
        self.proof_url = proof_url
        self.processed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_failed(self, reason: str) -> None:
        """Registra a falha na transferência bancária."""
        if not reason or not reason.strip():
            raise ValueError("Motivo da falha é obrigatório")
            
        self.status = PayoutStatus.FAILED
        self.failure_reason = reason.strip()
        self.updated_at = datetime.now(timezone.utc)