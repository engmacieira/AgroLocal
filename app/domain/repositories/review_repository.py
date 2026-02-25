from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.review import Review

class IReviewRepository(ABC):
    @abstractmethod
    def save(self, review: Review) -> Review:
        pass

    @abstractmethod
    def get_by_id(self, review_id: UUID) -> Optional[Review]:
        pass

    @abstractmethod
    def get_by_order_id(self, order_id: UUID) -> Optional[Review]:
        pass

    @abstractmethod
    def get_by_producer_id(self, producer_id: UUID, skip: int = 0, limit: int = 100) -> List[Review]:
        """Vitrine de reputação do produtor."""
        pass