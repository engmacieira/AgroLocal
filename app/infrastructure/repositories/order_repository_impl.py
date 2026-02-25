from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from app.domain.entities.order import Order, OrderItem
from app.domain.repositories.order_repository import IOrderRepository
from app.infrastructure.models.order_model import OrderModel, OrderItemModel

class OrderRepositoryImpl(IOrderRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: OrderModel) -> Order:
        domain_items = []
        for item_model in model.items:
            item = OrderItem(
                id=item_model.id,
                product_id=item_model.product_id,
                product_name_snapshot=item_model.product_name_snapshot,
                unit_snapshot=item_model.unit_snapshot,
                unit_price_snapshot=Decimal(str(item_model.unit_price_snapshot)),
                quantity=item_model.quantity
            )
            # Como o subtotal é preenchido no __post_init__, nós garantimos que bate com o banco
            domain_items.append(item)

        return Order(
            id=model.id,
            customer_id=model.customer_id,
            producer_id=model.producer_id,
            delivery_type=model.delivery_type,
            delivery_fee=Decimal(str(model.delivery_fee)),
            status=model.status,
            total_amount=Decimal(str(model.total_amount)),
            cancellation_reason=model.cancellation_reason,
            created_at=model.created_at,
            updated_at=model.updated_at,
            items=domain_items
        )

    def save(self, order: Order) -> Order:
        # Prepara o modelo do Pedido
        model = OrderModel(
            id=order.id, customer_id=order.customer_id, producer_id=order.producer_id,
            status=order.status, cancellation_reason=order.cancellation_reason,
            total_amount=order.total_amount, delivery_type=order.delivery_type,
            delivery_fee=order.delivery_fee, created_at=order.created_at, updated_at=order.updated_at
        )

        # Prepara os modelos dos Itens
        model.items = [
            OrderItemModel(
                id=item.id, order_id=order.id, product_id=item.product_id,
                product_name_snapshot=item.product_name_snapshot, unit_snapshot=item.unit_snapshot,
                unit_price_snapshot=item.unit_price_snapshot, quantity=item.quantity, subtotal=item.subtotal
            ) for item in order.items
        ]

        self.db.merge(model)
        self.db.commit()
        return order

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        model = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        return self._to_domain(model) if model else None

    def get_by_customer_id(self, customer_id: UUID, skip: int = 0, limit: int = 100) -> List[Order]:
        models = self.db.query(OrderModel).filter(OrderModel.customer_id == customer_id).order_by(OrderModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models]

    def get_by_producer_id(self, producer_id: UUID, skip: int = 0, limit: int = 100) -> List[Order]:
        models = self.db.query(OrderModel).filter(OrderModel.producer_id == producer_id).order_by(OrderModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models]