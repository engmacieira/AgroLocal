import pytest
import uuid
from decimal import Decimal
from typing import List, Optional
from app.domain.entities.producer_product import ProducerProduct, AvailabilityType, DeliveryType
from app.domain.repositories.producer_product_repository import IProducerProductRepository
from app.application.use_cases.offer_management import (
    CreateOfferUseCase, CreateOfferDTO,
    UpdateStockUseCase, UpdateOfferUseCase, UpdateOfferDTO,
    UpdateDeliveryOptionsUseCase, DeliveryOptionDTO, AddOfferImageUseCase
)

# 1. O Dublê de Testes (Fake Repository)
class FakeProducerProductRepository(IProducerProductRepository):
    def __init__(self):
        self.offers: List[ProducerProduct] = []

    def save(self, offer: ProducerProduct) -> ProducerProduct:
        existing = self.get_by_id(offer.id)
        if existing:
            self.offers.remove(existing)
        self.offers.append(offer)
        return offer

    def get_by_id(self, offer_id: uuid.UUID) -> Optional[ProducerProduct]:
        return next((o for o in self.offers if o.id == offer_id), None)

    def get_by_producer_id(self, producer_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[ProducerProduct]:
        return [o for o in self.offers if o.producer_id == producer_id and o.is_active]

    def get_by_global_product_id(self, global_product_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[ProducerProduct]:
        return [o for o in self.offers if o.global_product_id == global_product_id and o.is_active]

    def delete(self, offer_id: uuid.UUID) -> None:
        offer = self.get_by_id(offer_id)
        if offer:
            offer.deactivate()

# 2. Testes dos Casos de Uso

def test_deve_criar_nova_oferta():
    fake_repo = FakeProducerProductRepository()
    use_case = CreateOfferUseCase(fake_repo)
    
    dto = CreateOfferDTO(
        producer_id=uuid.uuid4(),
        global_product_id=uuid.uuid4(),
        price=Decimal("15.50"),
        unit="kg",
        stock_quantity=100.0,
        description="Tomate fresquinho"
    )
    
    oferta = use_case.execute(dto)
    
    assert oferta.price == Decimal("15.50")
    assert oferta.stock_quantity == 100.0
    assert len(fake_repo.offers) == 1

def test_deve_atualizar_estoque_da_oferta():
    fake_repo = FakeProducerProductRepository()
    oferta = fake_repo.save(ProducerProduct(
        producer_id=uuid.uuid4(), global_product_id=uuid.uuid4(),
        price=Decimal("10.00"), stock_quantity=50.0
    ))
    
    use_case = UpdateStockUseCase(fake_repo)
    # Adiciona 20 ao estoque
    oferta_atualizada = use_case.execute(offer_id=oferta.id, add_quantity=20.0)
    
    assert oferta_atualizada.stock_quantity == 70.0

def test_nao_deve_atualizar_estoque_de_oferta_inexistente():
    fake_repo = FakeProducerProductRepository()
    use_case = UpdateStockUseCase(fake_repo)
    
    with pytest.raises(ValueError, match="Oferta não encontrada"):
        use_case.execute(offer_id=uuid.uuid4(), add_quantity=10.0)

def test_deve_atualizar_preco_da_oferta():
    fake_repo = FakeProducerProductRepository()
    oferta = fake_repo.save(ProducerProduct(
        producer_id=uuid.uuid4(), global_product_id=uuid.uuid4(),
        price=Decimal("10.00")
    ))
    
    use_case = UpdateOfferUseCase(fake_repo)
    dto = UpdateOfferDTO(offer_id=oferta.id, new_price=Decimal("12.00"), new_description="Promoção!")
    
    oferta_atualizada = use_case.execute(dto)
    
    assert oferta_atualizada.price == Decimal("12.00")
    assert oferta_atualizada.description == "Promoção!"
    
def test_deve_atualizar_opcoes_de_entrega_da_oferta():
    fake_repo = FakeProducerProductRepository()
    oferta = fake_repo.save(ProducerProduct(
        producer_id=uuid.uuid4(), global_product_id=uuid.uuid4(), price=Decimal("10.00")
    ))

    use_case = UpdateDeliveryOptionsUseCase(fake_repo)
    dtos = [
        DeliveryOptionDTO(delivery_type=DeliveryType.DOMICILIO, fee=Decimal("5.00"), schedule="Sábados")
    ]

    oferta_atualizada = use_case.execute(offer_id=oferta.id, options_dto=dtos)

    assert len(oferta_atualizada.delivery_options) == 1
    assert oferta_atualizada.delivery_options[0].fee == Decimal("5.00")

def test_deve_adicionar_imagem_na_oferta():
    fake_repo = FakeProducerProductRepository()
    oferta = fake_repo.save(ProducerProduct(
        producer_id=uuid.uuid4(), global_product_id=uuid.uuid4(), price=Decimal("10.00")
    ))

    use_case = AddOfferImageUseCase(fake_repo)
    oferta_atualizada = use_case.execute(offer_id=oferta.id, url="http://s3.com/foto.jpg", is_primary=True)

    assert len(oferta_atualizada.images) == 1
    assert oferta_atualizada.images[0].url == "http://s3.com/foto.jpg"
    assert oferta_atualizada.images[0].is_primary is True