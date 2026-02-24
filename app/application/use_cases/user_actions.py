from uuid import UUID
from app.domain.repositories.user_repository import IUserRepository

class AcceptTermsUseCase:
    """Caso de Uso: Registra o aceite dos termos de uso (LGPD)."""
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> None:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        
        user.accept_terms() # Regra de negócio pura!
        self.user_repository.save(user)

class VerifyAccountUseCase:
    """Caso de Uso: Confirma a conta/telefone do usuário."""
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> None:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
            
        user.verify_account() # Regra de negócio pura!
        self.user_repository.save(user)