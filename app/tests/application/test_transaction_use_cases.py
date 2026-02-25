import pytest
import uuid
from decimal import Decimal
from typing import List, Optional
from app.domain.entities.order import Order, OrderStatus, DeliveryType
from app.domain.entities.transaction import Transaction, TransactionStatus, PaymentMethod
from app.domain.repositories.order_repository import IOrderRepository
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.application.use_cases.transaction_management import GeneratePaymentUseCase, ProcessWebhookUseCase

# --- FAKE REPOSITORIES ---
class FakeOrderRepository(IOrderRepository):
    def __init__(self): self.orders = []
    def save(self, order): return order
    def get_by_id(self, order_id): return next((o for o in self.orders if o.id == order_id), None)
    def get_by_customer_id(self, customer_id, skip=0, limit=100): pass
    def get_by_producer_id(self, producer_id, skip=0, limit=100): pass

class FakeTransactionRepository(ITransactionRepository):
    def __init__(self): self.transactions = []
    def save(self, transaction): 
        self.transactions.append(transaction)
        return transaction
    def get_by_id(self, transaction_id): return next((t for t in self.transactions if t.id == transaction_id), None)
    def get_by_external_id(self, external_id): pass

# --- TESTES ---
def test_deve_gerar_pagamento_unificado_com_sucesso():
    order_repo = FakeOrderRepository()
    trans_repo = FakeTransactionRepository()
    
    # Prepara um pedido válido
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("50.00"))
    order_repo.orders.append(pedido)
    
    use_case = GeneratePaymentUseCase(trans_repo, order_repo)
    transacao = use_case.execute(order_ids=[pedido.id])
    
    assert transacao.amount == Decimal("50.00")
    assert transacao.status == TransactionStatus.PENDING
    assert transacao.pix_copy_paste is not None

def test_nao_deve_gerar_pagamento_se_pedido_ja_estiver_pago():
    order_repo = FakeOrderRepository()
    trans_repo = FakeTransactionRepository()
    
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("50.00"))
    pedido.status = OrderStatus.PAID # Simulando um pedido que já foi pago
    order_repo.orders.append(pedido)
    
    use_case = GeneratePaymentUseCase(trans_repo, order_repo)
    
    with pytest.raises(ValueError, match="já não está pendente"):
        use_case.execute(order_ids=[pedido.id])

def test_deve_processar_webhook_e_aprovar_pagamento():
    trans_repo = FakeTransactionRepository()
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("50.00"))
    transacao = Transaction(payment_method=PaymentMethod.PIX, orders=[pedido])
    trans_repo.transactions.append(transacao)
    
    use_case = ProcessWebhookUseCase(trans_repo)
    trans_atualizada = use_case.execute(
        transaction_id=transacao.id, 
        external_id="MP-98765", 
        is_approved=True
    )
    
    assert trans_atualizada.status == TransactionStatus.APPROVED
    assert trans_atualizada.external_transaction_id == "MP-98765"
    assert pedido.status == OrderStatus.PAID # Confirma a cascata para o pedido