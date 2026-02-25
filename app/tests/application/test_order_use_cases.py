import pytest
import uuid
from decimal import Decimal
from typing import List, Optional
from app.domain.entities.order import Order, DeliveryType
from app.domain.entities.producer_product import ProducerProduct, DeliveryOption, AvailabilityType
from app.domain.entities.catalog import GlobalProduct
from app.domain.repositories.order_repository import IOrderRepository
from app.domain.repositories.producer_product_repository import IProducerProductRepository
from app.domain.repositories.catalog_repository import IGlobalProductRepository
from app.application.use_cases.checkout_management import (
    CheckoutUseCase, CheckoutCartDTO, CheckoutProducerGroupDTO, CheckoutItemDTO
)

# --- FAKE REPOSITORIES (Dublês para rodar em milissegundos) ---
class FakeOrderRepository(IOrderRepository):
    def __init__(self): self.orders: List[Order] = []
    def save(self, order: Order) -> Order:
        self.orders.append(order)
        return order
    def get_by_id(self, order_id: uuid.UUID): pass
    def get_by_customer_id(self, customer_id: uuid.UUID, skip=0, limit=100): return self.orders
    def get_by_producer_id(self, producer_id: uuid.UUID, skip=0, limit=100): return self.orders

class FakeProducerProductRepository(IProducerProductRepository):
    def __init__(self): self.offers = []
    def save(self, offer): return offer
    def get_by_id(self, offer_id): return next((o for o in self.offers if o.id == offer_id), None)
    def get_by_producer_id(self, producer_id, skip=0, limit=100): pass
    def get_by_global_product_id(self, global_product_id, skip=0, limit=100): pass
    def delete(self, offer_id): pass

class FakeGlobalProductRepository(IGlobalProductRepository):
    def __init__(self): self.products = []
    def save(self, product): return product
    def get_by_id(self, product_id): return next((p for p in self.products if p.id == product_id), None)
    def get_by_name(self, name): pass
    def get_all_by_status(self, status, skip=0, limit=100): pass
    def get_by_category(self, category_id, skip=0, limit=100): pass
    def search_by_text(self, query, skip=0, limit=100): pass

# --- TESTES DO CHECKOUT ---
def test_deve_processar_checkout_com_frete_maximo_e_reserva_de_estoque():
    # 1. Preparação (Massa de Dados)
    order_repo = FakeOrderRepository()
    offer_repo = FakeProducerProductRepository()
    catalog_repo = FakeGlobalProductRepository()
    
    produtor_id = uuid.uuid4()
    produto_global_id = uuid.uuid4()
    
    # Criamos o nome real no Catálogo Mestre
    catalog_repo.products.append(GlobalProduct(id=produto_global_id, name="Tomate Carmem", category_id=uuid.uuid4()))
    
    # Criamos 2 ofertas do mesmo produtor
    oferta_1 = ProducerProduct(id=uuid.uuid4(), producer_id=produtor_id, global_product_id=produto_global_id, price=Decimal("10.00"), stock_quantity=50.0)
    oferta_1.set_delivery_options([DeliveryOption(delivery_type=DeliveryType.DOMICILIO, fee=Decimal("5.00"))])
    
    oferta_2 = ProducerProduct(id=uuid.uuid4(), producer_id=produtor_id, global_product_id=produto_global_id, price=Decimal("15.00"), stock_quantity=20.0)
    oferta_2.set_delivery_options([DeliveryOption(delivery_type=DeliveryType.DOMICILIO, fee=Decimal("12.00"))]) # Frete mais caro!
    
    offer_repo.offers.extend([oferta_1, oferta_2])
    
    # 2. Ação (O cliente envia o carrinho agrupado por produtor)
    use_case = CheckoutUseCase(order_repo, offer_repo, catalog_repo)
    
    cart = CheckoutCartDTO(
        customer_id=uuid.uuid4(),
        groups=[
            CheckoutProducerGroupDTO(
                producer_id=produtor_id,
                delivery_type=DeliveryType.DOMICILIO,
                items=[
                    CheckoutItemDTO(offer_id=oferta_1.id, quantity=2.0), # 2 x 10 = 20
                    CheckoutItemDTO(offer_id=oferta_2.id, quantity=1.0)  # 1 x 15 = 15
                ]
            )
        ]
    )
    
    pedidos = use_case.execute(cart)
    
    # 3. Asserções (Verificações)
    assert len(pedidos) == 1 # Um único pedido para este produtor
    pedido = pedidos[0]
    
    # Verifica o Frete Máximo (Deve ser 12.00 e não a soma 17.00)
    assert pedido.delivery_fee == Decimal("12.00")
    
    # Verifica Subtotal e Total (20 + 15 + 12 = 47)
    assert pedido.total_amount == Decimal("47.00")
    
    # Verifica Snapshot Fiscal
    assert pedido.items[0].product_name_snapshot == "Tomate Carmem"
    
    # Verifica a reserva de estoque (-2 e -1)
    assert oferta_1.stock_quantity == 48.0
    assert oferta_2.stock_quantity == 19.0