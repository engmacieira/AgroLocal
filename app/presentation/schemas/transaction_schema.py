from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from app.domain.entities.transaction import PaymentMethod, TransactionStatus

# --- REQUESTS ---

class GeneratePaymentRequest(BaseModel):
    order_ids: List[UUID]
    payment_method: PaymentMethod = PaymentMethod.PIX

class WebhookPayloadRequest(BaseModel):
    """Simula o payload enviado pelo Gateway de Pagamento."""
    external_transaction_id: str
    is_approved: bool
    failure_reason: Optional[str] = None

# --- RESPONSES ---

class TransactionResponse(BaseModel):
    id: UUID
    payment_method: PaymentMethod
    amount: Decimal
    status: TransactionStatus
    external_transaction_id: Optional[str]
    pix_copy_paste: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)