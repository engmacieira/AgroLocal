from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.producer_profile import ProducerProfile

class IProducerRepository(ABC):
    """
    Contrato obrigatório para a persistência do Perfil de Produtor.
    """

    @abstractmethod
    def save(self, profile: ProducerProfile) -> ProducerProfile:
        """Cria um novo perfil ou atualiza um existente."""
        pass

    @abstractmethod
    def get_by_id(self, profile_id: UUID) -> Optional[ProducerProfile]:
        """Busca um perfil específico pelo seu ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UUID) -> Optional[ProducerProfile]:
        """Busca o perfil de produtor vinculado a um utilizador (Relação 1:1)."""
        pass
        
    @abstractmethod
    def get_by_document(self, document: str) -> Optional[ProducerProfile]:
        """Busca para evitar CPFs/CNPJs duplicados no sistema."""
        pass

    @abstractmethod
    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[ProducerProfile]:
        """Lista produtores ativos (Para a vitrine do marketplace)."""
        pass

    @abstractmethod
    def delete(self, profile_id: UUID) -> None:
        """Aplica soft delete no perfil."""
        pass