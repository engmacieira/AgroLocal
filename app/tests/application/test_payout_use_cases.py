import pytest
import uuid
from decimal import Decimal
from app.domain.entities.order import Order, OrderStatus, DeliveryType
from app.domain.entities.payout import Payout, PayoutStatus
from app.domain.repositories.order_repository import IOrderRepository
from app.domain.repositories.payout_repository import IPayoutRepository
from app.application.use_cases.payout_management import SchedulePayoutUseCase, ProcessPayoutUseCase, FailPayoutUseCase

# --- FAKE REPOSITORIES ---
class FakeOrderRepository(IOrderRepository):
    def __init__(self): self.orders = []
    def save(self, order):
        self.orders = [o for o in self.orders if o.id != order.id] # Remove o antigo se existir
        self.orders.append(order)
        return order
    def get_by_id(self, order_id): return next((o for o in self.orders if o.id == order_id), None)
    def get_by_customer_id(self, customer_id, skip=0, limit=100): pass
    def get_by_producer_id(self, producer_id, skip=0, limit=100): pass

class FakePayoutRepository(IPayoutRepository):
    def __init__(self): self.payouts = []
    def save(self, payout):
        self.payouts = [p for p in self.payouts if p.id != payout.id]
        self.payouts.append(payout)
        return payout
    def get_by_id(self, payout_id): return next((p for p in self.payouts if p.id == payout_id), None)
    def get_by_order_id(self, order_id): return next((p for p in self.payouts if p.order_id == order_id), None)
    def get_pending_by_producer(self, producer_id): pass

# --- TESTES ---
def test_deve_agendar_repasse_com_calculo_de_comissao_correto():
    order_repo = FakeOrderRepository()
    payout_repo = FakePayoutRepository()

    # Pedido de R$ 150.00
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("150.00"))
    pedido.status = OrderStatus.DELIVERED
    order_repo.save(pedido)

    use_case = SchedulePayoutUseCase(payout_repo, order_repo)
    # Mandamos agendar com uma taxa customizada de 10%
    repasse = use_case.execute(order_id=pedido.id, target_pix_key="pix@teste.com", fee_percentage=Decimal("10.00"))

    assert repasse.amount_gross == Decimal("150.00")
    assert repasse.amount_fee == Decimal("15.00") # 10% de 150
    assert repasse.amount_net == Decimal("135.00") # O que sobra para o produtor
    assert repasse.status == PayoutStatus.SCHEDULED

def test_deve_processar_repasse_e_finalizar_pedido_em_cascata():
    order_repo = FakeOrderRepository()
    payout_repo = FakePayoutRepository()

    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("100.00"))
    pedido.status = OrderStatus.DELIVERED
    order_repo.save(pedido)

    repasse = Payout(order_id=pedido.id, producer_id=pedido.producer_id, target_pix_key_snapshot="pix", amount_gross=Decimal("100.00"), amount_fee=Decimal("10.00"))
    payout_repo.save(repasse)

    use_case = ProcessPayoutUseCase(payout_repo, order_repo)
    repasse_pago = use_case.execute(payout_id=repasse.id, bank_transaction_id="PIX-E2E-12345", proof_url="http://s3.com/recibo.pdf")

    assert repasse_pago.status == PayoutStatus.PAID
    assert repasse_pago.bank_transaction_id == "PIX-E2E-12345"

    # Confirmação da Regra de Negócio: O pedido avançou para COMPLETED?
    pedido_atualizado = order_repo.get_by_id(pedido.id)
    assert pedido_atualizado.status == OrderStatus.COMPLETED

def test_deve_falhar_repasse_com_motivo():
    payout_repo = FakePayoutRepository()
    repasse = Payout(order_id=uuid.uuid4(), producer_id=uuid.uuid4(), target_pix_key_snapshot="pix", amount_gross=Decimal("100.00"), amount_fee=Decimal("10.00"))
    payout_repo.save(repasse)

    use_case = FailPayoutUseCase(payout_repo)
    repasse_falho = use_case.execute(payout_id=repasse.id, reason="Chave PIX Cancelada")

    assert repasse_falho.status == PayoutStatus.FAILED
    assert repasse_falho.failure_reason == "Chave PIX Cancelada"