import uuid
from decimal import Decimal
from typing import List, Optional
from dataclasses import dataclass
from app.domain.entities.order import Order, DeliveryType
from app.domain.repositories.order_repository import IOrderRepository
from app.domain.repositories.producer_product_repository import IProducerProductRepository
from app.domain.repositories.catalog_repository import IGlobalProductRepository

@dataclass
class CheckoutItemDTO:
    offer_id: uuid.UUID
    quantity: float

@dataclass
class CheckoutProducerGroupDTO:
    """Itens comprados de um produtor específico, com a modalidade de entrega escolhida para ele."""
    producer_id: uuid.UUID
    delivery_type: DeliveryType
    items: List[CheckoutItemDTO]

@dataclass
class CheckoutCartDTO:
    """O Carrinho de Compras global do cliente."""
    customer_id: uuid.UUID
    groups: List[CheckoutProducerGroupDTO]

class CheckoutUseCase:
    """
    Orquestrador Central de Vendas.
    Transforma um carrinho numa lista de pedidos (Split), calculando fretes inteligentes e reservando estoque.
    """
    def __init__(
        self, 
        order_repository: IOrderRepository, 
        offer_repository: IProducerProductRepository,
        catalog_repository: IGlobalProductRepository
    ):
        self.order_repository = order_repository
        self.offer_repository = offer_repository
        self.catalog_repository = catalog_repository

    def execute(self, cart_dto: CheckoutCartDTO) -> List[Order]:
        created_orders = []

        for group in cart_dto.groups:
            if not group.items:
                continue

            max_delivery_fee = Decimal("0.00")
            
            # Cria a estrutura base do Pedido para este produtor
            order = Order(
                customer_id=cart_dto.customer_id,
                producer_id=group.producer_id,
                delivery_type=group.delivery_type
            )

            for item_dto in group.items:
                # 1. Busca a Oferta e Valida
                offer = self.offer_repository.get_by_id(item_dto.offer_id)
                if not offer or not offer.is_active:
                    raise ValueError(f"A oferta com ID {item_dto.offer_id} está indisponível.")
                
                if offer.producer_id != group.producer_id:
                    raise ValueError("Inconsistência no carrinho: item não pertence a este produtor.")

                # 2. Valida a Logística e Encontra o Maior Frete
                delivery_opt = next((opt for opt in offer.delivery_options if opt.delivery_type == group.delivery_type and opt.is_enabled), None)
                if not delivery_opt:
                    raise ValueError(f"O produto selecionado não suporta a entrega: {group.delivery_type.value}")

                max_delivery_fee = max(max_delivery_fee, delivery_opt.fee)

                # 3. Reserva de Estoque Imediata (Levanta exceção se não houver saldo)
                offer.update_stock(-item_dto.quantity)
                self.offer_repository.save(offer) # Persiste a baixa no estoque imediatamente

                # 4. Busca o Nome Real (Catálogo) para o Snapshot Fiscal
                global_product = self.catalog_repository.get_by_id(offer.global_product_id)
                product_name = global_product.name if global_product else "Produto Desconhecido"

                # 5. Adiciona o Item (Snapshot)
                order.add_item(
                    product_id=offer.id,
                    product_name_snapshot=product_name,
                    unit_snapshot=offer.unit,
                    unit_price_snapshot=offer.price,
                    quantity=item_dto.quantity
                )

            # 6. Aplica a Regra do Frete Único (Maior Valor) e Finaliza
            order.set_delivery_fee(max_delivery_fee)
            saved_order = self.order_repository.save(order)
            created_orders.append(saved_order)

        return created_orders
    
class UpdateOrderStatusUseCase:
    """Caso de Uso: Avança a máquina de estados do pedido."""
    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id: uuid.UUID, action: str, reason: Optional[str] = None) -> Order:
        pedido = self.order_repository.get_by_id(order_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        
        action = action.upper()
        if action == "PAID":
            pedido.mark_as_paid()
        elif action == "PREPARING":
            pedido.start_preparing()
        elif action == "READY":
            pedido.mark_as_ready()
        elif action == "DELIVERED":
            pedido.mark_as_delivered()
        elif action == "CANCELED":
            pedido.cancel(reason=reason or "")
        else:
            raise ValueError(f"Ação de status inválida: {action}")
        
        return self.order_repository.save(pedido)