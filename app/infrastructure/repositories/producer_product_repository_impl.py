from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from app.domain.entities.producer_product import ProducerProduct, ProductImage, DeliveryOption, DeliveryType
from app.domain.repositories.producer_product_repository import IProducerProductRepository
from app.infrastructure.models.product_model import ProducerProductModel, ProductImageModel, OfferDeliveryOptionModel

class ProducerProductRepositoryImpl(IProducerProductRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: ProducerProductModel) -> ProducerProduct:
        # 1. Converte as imagens
        domain_images = [
            ProductImage(id=img.id, url=img.url, is_primary=img.is_primary, created_at=img.created_at)
            for img in model.images
        ]
        
        # Converte as opções de entrega
        domain_deliveries = [
            DeliveryOption(id=opt.id, delivery_type=opt.delivery_type, fee=Decimal(str(opt.fee)), schedule=opt.schedule, is_enabled=opt.is_enabled)
            for opt in model.delivery_options
        ]
        
        # 2. Converte a Oferta Principal
        return ProducerProduct(
            id=model.id,
            producer_id=model.producer_id,
            global_product_id=model.global_product_id,
            price=Decimal(str(model.price)), # Garante que o Numeric volta como Decimal
            unit=model.unit,
            stock_quantity=model.stock_quantity,
            minimum_order_quantity=model.minimum_order_quantity,
            availability_type=model.availability_type,
            description=model.description,
            harvest_date=model.harvest_date,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
            images=domain_images,
            delivery_options=domain_deliveries
        )

    def save(self, offer: ProducerProduct) -> ProducerProduct:
        # Converte Entidade para Modelo
        model = ProducerProductModel(
            id=offer.id, producer_id=offer.producer_id, global_product_id=offer.global_product_id,
            price=offer.price, unit=offer.unit, stock_quantity=offer.stock_quantity,
            minimum_order_quantity=offer.minimum_order_quantity, availability_type=offer.availability_type,
            description=offer.description, harvest_date=offer.harvest_date,
            is_active=offer.is_active, created_at=offer.created_at, updated_at=offer.updated_at
        )
        
        # Converte as imagens
        model_images = [
            ProductImageModel(id=img.id, producer_product_id=offer.id, url=img.url, is_primary=img.is_primary, created_at=img.created_at)
            for img in offer.images
        ]
        model.images = model_images

        model.delivery_options = [
            OfferDeliveryOptionModel(id=opt.id, producer_product_id=offer.id, delivery_type=opt.delivery_type, fee=opt.fee, schedule=opt.schedule, is_enabled=opt.is_enabled)
            for opt in offer.delivery_options
        ]
        
        self.db.merge(model)
        self.db.commit()
        return offer

    def get_by_id(self, offer_id: UUID) -> Optional[ProducerProduct]:
        model = self.db.query(ProducerProductModel).filter(ProducerProductModel.id == offer_id).first()
        return self._to_domain(model) if model else None

    def get_by_producer_id(self, producer_id: UUID, skip: int = 0, limit: int = 100) -> List[ProducerProduct]:
        models = self.db.query(ProducerProductModel).filter(
            ProducerProductModel.producer_id == producer_id,
            ProducerProductModel.is_active == True
        ).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models]

    def get_by_global_product_id(self, global_product_id: UUID, skip: int = 0, limit: int = 100) -> List[ProducerProduct]:
        models = self.db.query(ProducerProductModel).filter(
            ProducerProductModel.global_product_id == global_product_id,
            ProducerProductModel.is_active == True
        ).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models]

    def delete(self, offer_id: UUID) -> None:
        offer = self.get_by_id(offer_id)
        if offer:
            offer.deactivate()
            self.save(offer)