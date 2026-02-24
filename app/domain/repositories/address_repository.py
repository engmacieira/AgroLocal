from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.address import Address

class IAddressRepository(ABC):
    """
    Interface do Repositório de Endereços.
    Define o contrato obrigatório para qualquer banco de dados que for armazenar endereços.
    """

    @abstractmethod
    def save(self, address: Address) -> Address:
        """Salva um novo endereço ou atualiza um existente."""
        pass

    @abstractmethod
    def get_by_id(self, address_id: UUID) -> Optional[Address]:
        """Busca um endereço específico pelo seu ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Address]:
        """Busca todos os endereços ativos de um usuário específico."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Address]:
        """Busca todos os endereços ativos do sistema (Geral/Admin)."""
        pass
    
    @abstractmethod
    def delete(self, address_id: UUID) -> None:
        """Aplica soft delete em um endereço."""
        pass