import pytest
import uuid
from decimal import Decimal
from app.domain.entities.order import Order, OrderStatus, DeliveryType
from app.domain.entities.review import Review
from app.domain.repositories.order_repository import IOrderRepository
from app.domain.repositories.review_repository import IReviewRepository
from app.application.use_cases.review_management import CreateReviewUseCase

# --- FAKE REPOSITORIES ---
class FakeOrderRepository(IOrderRepository):
    def __init__(self): self.orders = []
    def save(self, order): return order
    def get_by_id(self, order_id): return next((o for o in self.orders if o.id == order_id), None)
    def get_by_customer_id(self, customer_id, skip=0, limit=100): pass
    def get_by_producer_id(self, producer_id, skip=0, limit=100): pass

class FakeReviewRepository(IReviewRepository):
    def __init__(self): self.reviews = []
    def save(self, review): 
        self.reviews.append(review)
        return review
    def get_by_id(self, review_id): return next((r for r in self.reviews if r.id == review_id), None)
    def get_by_order_id(self, order_id): return next((r for r in self.reviews if r.order_id == order_id), None)
    def get_by_producer_id(self, producer_id, skip=0, limit=100): pass

# --- TESTES ---
def test_deve_criar_avaliacao_para_pedido_entregue():
    order_repo = FakeOrderRepository()
    review_repo = FakeReviewRepository()
    
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("50.00"))
    pedido.status = OrderStatus.DELIVERED
    order_repo.orders.append(pedido)
    
    use_case = CreateReviewUseCase(review_repo, order_repo)
    avaliacao = use_case.execute(order_id=pedido.id, customer_id=pedido.customer_id, rating=5, comment="Excelente")
    
    assert avaliacao.rating == 5
    assert avaliacao.comment == "Excelente"

def test_nao_deve_avaliar_pedido_nao_entregue():
    order_repo = FakeOrderRepository()
    review_repo = FakeReviewRepository()
    
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("50.00"))
    pedido.status = OrderStatus.PREPARING # Ainda não foi entregue!
    order_repo.orders.append(pedido)
    
    use_case = CreateReviewUseCase(review_repo, order_repo)
    
    with pytest.raises(ValueError, match="Apenas pedidos entregues"):
        use_case.execute(order_id=pedido.id, customer_id=pedido.customer_id, rating=5)

def test_nao_deve_permitir_duas_avaliacoes_no_mesmo_pedido():
    order_repo = FakeOrderRepository()
    review_repo = FakeReviewRepository()
    
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("50.00"))
    pedido.status = OrderStatus.DELIVERED
    order_repo.orders.append(pedido)
    
    use_case = CreateReviewUseCase(review_repo, order_repo)
    
    # Primeira avaliação (Sucesso)
    use_case.execute(order_id=pedido.id, customer_id=pedido.customer_id, rating=5)
    
    # Segunda avaliação no mesmo pedido (Falha)
    with pytest.raises(ValueError, match="já foi avaliado"):
        use_case.execute(order_id=pedido.id, customer_id=pedido.customer_id, rating=1)

def test_nao_deve_permitir_que_outro_usuario_avalie_o_pedido():
    order_repo = FakeOrderRepository()
    review_repo = FakeReviewRepository()
    
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("50.00"))
    pedido.status = OrderStatus.DELIVERED
    order_repo.orders.append(pedido)
    
    use_case = CreateReviewUseCase(review_repo, order_repo)
    
    outro_cliente_id = uuid.uuid4()
    with pytest.raises(ValueError, match="Você só pode avaliar os seus próprios pedidos"):
        use_case.execute(order_id=pedido.id, customer_id=outro_cliente_id, rating=5)