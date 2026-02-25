from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from app.domain.entities.payout import PayoutStatus

# --- REQUESTS ---

class SchedulePayoutRequest(BaseModel):
    order_id: UUID
    target_pix_key: str = Field(..., description="A chave PIX do produtor no momento do repasse")
    fee_percentage: Decimal = Field(default=Decimal("10.00"), description="A taxa da plataforma em %")

class ProcessPayoutRequest(BaseModel):
    bank_transaction_id: str = Field(..., description="O End-to-End ID do PIX gerado pelo banco")
    proof_url: str = Field(..., description="Link para o PDF/Imagem do comprovante")

class FailPayoutRequest(BaseModel):
    reason: str = Field(..., min_length=5, description="Motivo claro da falha bancária")

# --- RESPONSES ---

class PayoutResponse(BaseModel):
    id: UUID
    order_id: UUID
    producer_id: UUID
    status: PayoutStatus
    amount_gross: Decimal
    amount_fee: Decimal
    amount_net: Decimal
    target_pix_key_snapshot: str
    scheduled_for: Optional[datetime]
    processed_at: Optional[datetime]
    bank_transaction_id: Optional[str]
    proof_url: Optional[str]
    failure_reason: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)