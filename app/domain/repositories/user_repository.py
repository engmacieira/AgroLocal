from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain.entities.user import User

class IUserRepository(ABC):
    """
    Interface (Contrato) do Repositório de Usuários.
    Define QUAIS operações o banco de dados deve suportar, 
    sem dizer COMO ele deve fazer isso.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """
        Salva um novo usuário ou atualiza um existente.
        Recebe a Entidade de Domínio e deve retornar a Entidade salva.
        """
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca um usuário pelo seu ID único."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Busca uma lista paginada de usuários."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo seu endereço de e-mail."""
        pass
        
    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        """Remove (ou aplica soft delete) em um usuário."""
        pass