from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.communication import Conversation

class ICommunicationRepository(ABC):
    @abstractmethod
    def save(self, conversation: Conversation) -> Conversation:
        pass

    @abstractmethod
    def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        pass

    @abstractmethod
    def get_conversations_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Conversation]:
        """Traz todos os chamados em que o utilizador é o iniciador ou o alvo."""
        pass