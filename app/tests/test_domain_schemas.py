# Arquivo: app/tests/test_domain_schemas.py

import pytest
from uuid import uuid4
from decimal import Decimal
from datetime import datetime
from pydantic import ValidationError

from app.models.address_model import AddressType
from app.models.transaction_model import PaymentMethod
from app.models.order_model import DeliveryType
from app.models.audit_model import AuditAction

from app.schemas.address_schema import AddressCreate
from app.schemas.review_schema import ReviewCreate
from app.schemas.transaction_schema import TransactionBase
from app.schemas.order_schema import OrderCreate
from app.schemas.payout_schema import PayoutBase
from app.schemas.audit_schema import AuditLogRead

# --- 1. Testes de Endereço (Address) ---
def test_address_valid_state():
    """Testa criação de endereço com estado válido (UF)."""
    payload = {
        "street": "Rua Teste",
        "number": "123",
        "neighborhood": "Bairro",
        "city": "Cidade",
        "state": "SP", # 2 letras = OK
        "postal_code": "12345-678",
        "address_type": "RESIDENCIAL"
    }
    addr = AddressCreate(**payload)
    assert addr.state == "SP"
    assert addr.address_type == AddressType.RESIDENCIAL

def test_address_invalid_state_length():
    """O Schema deve bloquear estados que não sejam sigla (2 chars)."""
    payload = {
        "street": "Rua Teste",
        "number": "123",
        "neighborhood": "Bairro",
        "city": "Cidade",
        "state": "SAO PAULO", # Errado! Deveria ser SP
        "postal_code": "12345-678"
    }
    with pytest.raises(ValidationError) as exc:
        AddressCreate(**payload)
    
    # Verifica se o erro aponta para o campo 'state'
    assert any(e["loc"] == ("state",) for e in exc.value.errors())

# --- 2. Testes de Avaliação (Review) ---
def test_review_rating_range():
    """Nota deve ser entre 1 e 5."""
    # Teste Válido
    rev = ReviewCreate(
        order_id=uuid4(), producer_id=uuid4(),
        rating=5, comment="Excelente"
    )
    assert rev.rating == 5

    # Teste Inválido (Nota 6)
    with pytest.raises(ValidationError):
        ReviewCreate(
            order_id=uuid4(), producer_id=uuid4(),
            rating=6, comment="Exagerado"
        )

    # Teste Inválido (Nota 0)
    with pytest.raises(ValidationError):
        ReviewCreate(
            order_id=uuid4(), producer_id=uuid4(),
            rating=0, comment="Péssimo"
        )

# --- 3. Testes de Transação (Transaction) ---
def test_transaction_decimal_valid():
    """Testa se o schema aceita e converte float/string corretamente para Decimal."""
    payload = {
        "order_id": uuid4(),
        "payment_method": "PIX",
        "amount": "100.55" # String com 2 casas é o ideal
    }
    tx = TransactionBase(**payload)
    assert isinstance(tx.amount, Decimal)
    assert tx.amount == Decimal("100.55")

def test_transaction_decimal_precision_error():
    """Garante que o schema BLOQUEIA valores com mais de 2 casas decimais."""
    payload = {
        "order_id": uuid4(),
        "payment_method": "PIX",
        "amount": 100.556 # 3 casas decimais (Inválido!)
    }
    # O teste SÓ passa se o Pydantic levantar ValidationError
    with pytest.raises(ValidationError) as exc:
        TransactionBase(**payload)
    
    # Confirma se o erro foi no campo 'amount'
    assert any(e["loc"] == ("amount",) for e in exc.value.errors())

# --- 4. Testes de Pedido (Order) ---
def test_order_structure():
    """Testa a estrutura aninhada de itens."""
    item_payload = {
        "product_id": uuid4(),
        "quantity": 2.5
    }
    order_payload = {
        "producer_id": uuid4(),
        "items": [item_payload],
        "delivery_type": "RETIRADA",
        "delivery_address_snapshot": "Rua tal, 123"
    }
    order = OrderCreate(**order_payload)
    assert len(order.items) == 1
    assert order.items[0].quantity == 2.5
    assert order.delivery_type == DeliveryType.RETIRADA

# --- 5. Testes de Repasse (Payout) ---
def test_payout_calculations_schema():
    """Verifica se o schema aceita os valores calculados."""
    payload = {
        "order_id": uuid4(),
        "producer_id": uuid4(),
        "amount_gross": 100.00,
        "amount_fee": 10.00,
        "amount_net": 90.00,
        "target_pix_key_snapshot": "chave@pix.com"
    }
    payout = PayoutBase(**payload)
    assert payout.amount_net == Decimal("90.00")

# --- 6. Testes de Auditoria (Audit) ---
def test_audit_log_read_schema():
    """Testa a leitura de logs com JSON dinâmico."""
    data = {
        "id": uuid4(),
        "table_name": "users",
        "record_id": uuid4(), # Schema espera UUID
        "action": "CREATE",
        "created_at": datetime.now(),
        "old_values": None,
        "new_values": {"email": "novo@email.com", "active": True}
    }
    log = AuditLogRead(**data)
    assert log.action == AuditAction.CREATE
    assert log.new_values["email"] == "novo@email.com"
    assert log.new_values["active"] is True