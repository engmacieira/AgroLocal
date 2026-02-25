from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.payout import Payout

class IPayoutRepository(ABC):
    @abstractmethod
    def save(self, payout: Payout) -> Payout:
        pass

    @abstractmethod
    def get_by_id(self, payout_id: UUID) -> Optional[Payout]:
        pass

    @abstractmethod
    def get_by_order_id(self, order_id: UUID) -> Optional[Payout]:
        pass

    @abstractmethod
    def get_pending_by_producer(self, producer_id: UUID) -> List[Payout]:
        """Busca repasses agendados ou em processamento para um produtor."""
        pass