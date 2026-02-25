from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.producer_product import ProducerProduct

class IProducerProductRepository(ABC):
    @abstractmethod
    def save(self, offer: ProducerProduct) -> ProducerProduct:
        """Salva uma nova oferta ou atualiza uma existente (incluindo imagens)."""
        pass

    @abstractmethod
    def get_by_id(self, offer_id: UUID) -> Optional[ProducerProduct]:
        """Busca uma oferta específica pelo ID."""
        pass

    @abstractmethod
    def get_by_producer_id(self, producer_id: UUID, skip: int = 0, limit: int = 100) -> List[ProducerProduct]:
        """Lista todas as ofertas (ativas) de um produtor específico (Vitrine da Lojinha)."""
        pass

    @abstractmethod
    def get_by_global_product_id(self, global_product_id: UUID, skip: int = 0, limit: int = 100) -> List[ProducerProduct]:
        """Busca quem está vendendo um determinado item global (Ex: 'Quem tem Tomate Carmem?')."""
        pass

    @abstractmethod
    def delete(self, offer_id: UUID) -> None:
        """Aplica soft delete na oferta (Pausa as vendas)."""
        pass