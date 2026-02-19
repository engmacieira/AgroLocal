from pydantic import Field, ConfigDict
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from app.models.transaction_model import TransactionStatus, PaymentMethod
from app.schemas.base_schema import BaseSchema, TimestampSchema

class TransactionBase(BaseSchema):
    """
    Schema base para Transações Financeiras (Pagamentos).
    Define o quanto será cobrado e as condições de pagamento.
    """
    order_id: UUID = Field(
        ..., 
        description="ID do pedido que está sendo pago"
    )
    
    payment_method: PaymentMethod = Field(
        ..., 
        description="Método de pagamento escolhido (PIX, Cartão)"
    )
    
    amount: Decimal = Field(
        ..., 
        gt=0, 
        decimal_places=2,
        description="Valor total da transação a ser processada pelo gateway",
        examples=[150.00]
    )
    
    installments: int = Field(
        default=1, 
        ge=1, 
        le=24,
        description="Número de parcelas (1 = À vista)",
        examples=[1]
    )

class TransactionCreate(TransactionBase):
    """
    Payload para iniciar um novo pagamento.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "order_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "payment_method": "PIX",
                    "amount": 150.00,
                    "installments": 1
                }
            ]
        }
    )

class TransactionRead(TransactionBase, TimestampSchema):
    """
    Detalhes da transação processada.
    Retorna os dados necessários para o usuário efetuar o pagamento (ex: QR Code PIX).
    """
    id: UUID = Field(description="ID único da transação")
    
    status: TransactionStatus = Field(
        description="Status atual do pagamento (PENDING, APPROVED, FAILED, etc)"
    )
    
    external_transaction_id: Optional[str] = Field(
        default=None,
        description="ID da transação no gateway de pagamento (MercadoPago/Stripe/Pagar.me)"
    )
    
    # --- Dados exclusivos para Pagamento via PIX ---
    
    pix_qr_code_base64: Optional[str] = Field(
        default=None,
        description="Imagem do QR Code em Base64 (para renderizar na tela do App)"
    )
    
    pix_copy_paste: Optional[str] = Field(
        default=None,
        description="Código 'Copia e Cola' do PIX (Payload string)"
    )
    
    pix_expiration: Optional[datetime] = Field(
        default=None,
        description="Data e hora limite para o pagamento ser efetuado antes de expirar"
    )
    
    # --- Auditoria de Erros ---
    
    failure_reason: Optional[str] = Field(
        default=None,
        description="Motivo da recusa (Ex: 'Saldo insuficiente', 'Cartão vencido')"
    )