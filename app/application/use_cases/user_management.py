from uuid import UUID
from typing import List, Optional
from dataclasses import dataclass
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository

class GetUserUseCase:
    """Caso de Uso: Buscar um usuário pelo ID."""
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        return user

class GetAllUsersUseCase:
    """Caso de Uso: Buscar todos os usuários (Paginado)."""
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repository.get_all(skip, limit)

@dataclass
class UpdateUserDTO:
    """DTO com os dados permitidos para atualização."""
    user_id: UUID
    full_name: Optional[str] = None
    phone: Optional[str] = None
    # Não permitimos atualizar email ou senha por aqui (Segurança!)

class UpdateUserUseCase:
    """Caso de Uso: Atualizar dados básicos do usuário."""
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, dto: UpdateUserDTO) -> User:
        # 1. Busca a Entidade
        user = self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        
        # 2. Atualiza apenas os campos fornecidos
        if dto.full_name:
            user.full_name = dto.full_name
        if dto.phone:
            user.phone = dto.phone
            
        # 3. Manda o repositório salvar as alterações
        return self.user_repository.save(user)

class DeleteUserUseCase:
    """Caso de Uso: Realiza o Soft Delete do usuário."""
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> None:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
            
        # O repositório já cuida de chamar o user.deactivate() e salvar
        self.user_repository.delete(user_id)