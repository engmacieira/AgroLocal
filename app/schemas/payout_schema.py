from pydantic import Field, ConfigDict
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from app.models.payout_model import PayoutStatus
from app.schemas.base_schema import BaseSchema, TimestampSchema

class PayoutBase(BaseSchema):
    """
    Schema base para o fluxo de Repasses (Saída de dinheiro).
    Representa a transferência de valores da Plataforma para o Produtor.
    """
    order_id: UUID = Field(
        ..., 
        description="ID do pedido que originou este pagamento"
    )
    
    producer_id: UUID = Field(
        ..., 
        description="ID do produtor (beneficiário) que receberá o valor"
    )
    
    amount_gross: Decimal = Field(
        ..., 
        ge=0,
        description="Valor Bruto da venda (Total pago pelo cliente)",
        examples=[100.50]
    )
    
    amount_fee: Decimal = Field(
        ..., 
        ge=0,
        description="Valor da Taxa de Serviço retida pela plataforma",
        examples=[10.05]
    )
    
    amount_net: Decimal = Field(
        ..., 
        ge=0,
        description="Valor Líquido a ser transferido (Bruto - Taxa)",
        examples=[90.45]
    )
    
    target_pix_key_snapshot: str = Field(
        ..., 
        max_length=100,
        description="Cópia da chave PIX do produtor no momento da compra (Imutável)",
        examples=["123.456.789-00", "email@produtor.com"]
    )

class PayoutRead(PayoutBase, TimestampSchema):
    """
    Visualização detalhada do repasse, incluindo status bancário e agendamento.
    """
    id: UUID = Field(description="ID único do registro de repasse")
    
    status: PayoutStatus = Field(
        description="Estado atual da transferência (SCHEDULED, PAID, FAILED, etc)"
    )
    
    scheduled_for: Optional[datetime] = Field(
        default=None,
        description="Data prevista para o depósito na conta do produtor"
    )
    
    processed_at: Optional[datetime] = Field(
        default=None,
        description="Data e hora real da efetivação bancária"
    )
    
    bank_transaction_id: Optional[str] = Field(
        default=None,
        description="ID da transação no banco/gateway (Comprovante End-to-End)"
    )
    
    proof_url: Optional[str] = Field(
        default=None,
        description="Link para o comprovante de transferência (PDF/Imagem)"
    )
    
    failure_reason: Optional[str] = Field(
        default=None,
        description="Motivo da falha (se status for FAILED)"
    )

    # Exemplo Rico para o Swagger
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                    "order_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "producer_id": "b2f4c810-1d2a-4f5b-9c8e-2a3b4c5d6e7f",
                    "amount_gross": 150.00,
                    "amount_fee": 15.00,
                    "amount_net": 135.00,
                    "target_pix_key_snapshot": "joao@fazenda.com",
                    "status": "PAID",
                    "scheduled_for": "2026-02-20T10:00:00Z",
                    "processed_at": "2026-02-20T10:05:00Z",
                    "bank_transaction_id": "E12345678202602201000"
                }
            ]
        }
    )