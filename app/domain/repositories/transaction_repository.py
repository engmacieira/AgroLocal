from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain.entities.transaction import Transaction

class ITransactionRepository(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> Transaction:
        """Salva a transação e atualiza os pedidos vinculados."""
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        pass

    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Optional[Transaction]:
        """Busca a transação pelo ID do Gateway (Webhook)."""
        pass