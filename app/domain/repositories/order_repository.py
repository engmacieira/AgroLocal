from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.order import Order

class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        """Salva ou atualiza um pedido e os seus itens."""
        pass

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Busca um pedido específico."""
        pass

    @abstractmethod
    def get_by_customer_id(self, customer_id: UUID, skip: int = 0, limit: int = 100) -> List[Order]:
        """Lista o histórico de compras de um cliente."""
        pass

    @abstractmethod
    def get_by_producer_id(self, producer_id: UUID, skip: int = 0, limit: int = 100) -> List[Order]:
        """Lista os pedidos recebidos por um produtor (O painel de vendas)."""
        pass