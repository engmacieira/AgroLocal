import uuid
from decimal import Decimal
from typing import List, Optional
from dataclasses import dataclass
from datetime import date
from app.domain.entities.producer_product import ProducerProduct, AvailabilityType, DeliveryType, DeliveryOption
from app.domain.repositories.producer_product_repository import IProducerProductRepository

@dataclass
class CreateOfferDTO:
    producer_id: uuid.UUID
    global_product_id: uuid.UUID
    price: Decimal
    unit: str = "kg"
    stock_quantity: float = 0.0
    minimum_order_quantity: float = 1.0
    availability_type: AvailabilityType = AvailabilityType.PRONTA_ENTREGA
    description: Optional[str] = None
    harvest_date: Optional[date] = None

class CreateOfferUseCase:
    """Caso de Uso: Produtor adiciona um produto à sua vitrine."""
    def __init__(self, offer_repository: IProducerProductRepository):
        self.offer_repository = offer_repository

    def execute(self, dto: CreateOfferDTO) -> ProducerProduct:
        # Nota: Numa versão mais complexa, poderíamos injetar o IGlobalProductRepository
        # aqui para verificar se o global_product_id existe e está APPROVED.
        
        nova_oferta = ProducerProduct(
            producer_id=dto.producer_id,
            global_product_id=dto.global_product_id,
            price=dto.price,
            unit=dto.unit,
            stock_quantity=dto.stock_quantity,
            minimum_order_quantity=dto.minimum_order_quantity,
            availability_type=dto.availability_type,
            description=dto.description,
            harvest_date=dto.harvest_date
        )
        return self.offer_repository.save(nova_oferta)

class UpdateStockUseCase:
    """Caso de Uso: Produtor movimenta o estoque (Venda ou Nova Colheita)."""
    def __init__(self, offer_repository: IProducerProductRepository):
        self.offer_repository = offer_repository

    def execute(self, offer_id: uuid.UUID, add_quantity: float) -> ProducerProduct:
        oferta = self.offer_repository.get_by_id(offer_id)
        if not oferta or not oferta.is_active:
            raise ValueError("Oferta não encontrada ou inativa")
            
        oferta.update_stock(add_quantity)
        return self.offer_repository.save(oferta)

@dataclass
class UpdateOfferDTO:
    offer_id: uuid.UUID
    new_price: Optional[Decimal] = None
    new_description: Optional[str] = None

class UpdateOfferUseCase:
    """Caso de Uso: Produtor atualiza os dados da vitrine (Preço/Descrição)."""
    def __init__(self, offer_repository: IProducerProductRepository):
        self.offer_repository = offer_repository

    def execute(self, dto: UpdateOfferDTO) -> ProducerProduct:
        oferta = self.offer_repository.get_by_id(dto.offer_id)
        if not oferta or not oferta.is_active:
            raise ValueError("Oferta não encontrada ou inativa")
            
        oferta.update_details(new_price=dto.new_price, new_description=dto.new_description)
        return self.offer_repository.save(oferta)

class GetProducerOffersUseCase:
    """Caso de Uso: Lista a vitrine de um produtor específico."""
    def __init__(self, offer_repository: IProducerProductRepository):
        self.offer_repository = offer_repository

    def execute(self, producer_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[ProducerProduct]:
        return self.offer_repository.get_by_producer_id(producer_id, skip, limit)
    
@dataclass
class DeliveryOptionDTO:
    delivery_type: DeliveryType
    fee: Decimal
    schedule: Optional[str] = None
    is_enabled: bool = True

class UpdateDeliveryOptionsUseCase:
    """Caso de Uso: Produtor define como o cliente pode receber o produto."""
    def __init__(self, offer_repository: IProducerProductRepository):
        self.offer_repository = offer_repository

    def execute(self, offer_id: uuid.UUID, options_dto: List[DeliveryOptionDTO]) -> ProducerProduct:
        oferta = self.offer_repository.get_by_id(offer_id)
        if not oferta or not oferta.is_active:
            raise ValueError("Oferta não encontrada ou inativa")
            
        domain_options = [
            DeliveryOption(
                delivery_type=opt.delivery_type, 
                fee=opt.fee, 
                schedule=opt.schedule, 
                is_enabled=opt.is_enabled
            ) for opt in options_dto
        ]
        
        oferta.set_delivery_options(domain_options)
        return self.offer_repository.save(oferta)

class AddOfferImageUseCase:
    """Caso de Uso: Produtor anexa uma foto real da sua colheita."""
    def __init__(self, offer_repository: IProducerProductRepository):
        self.offer_repository = offer_repository

    def execute(self, offer_id: uuid.UUID, url: str, is_primary: bool = False) -> ProducerProduct:
        oferta = self.offer_repository.get_by_id(offer_id)
        if not oferta or not oferta.is_active:
            raise ValueError("Oferta não encontrada ou inativa")
            
        oferta.add_image(url=url, is_primary=is_primary)
        return self.offer_repository.save(oferta)