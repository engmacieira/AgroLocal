import hashlib
from dataclasses import dataclass
from app.domain.repositories.user_repository import IUserRepository
from app.core.security import verify_password, create_access_token

@dataclass
class LoginDTO:
    email: str
    password: str

class AuthenticateUserUseCase:
    """Caso de Uso: Valida credenciais e gera o Token de Acesso."""
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, dto: LoginDTO) -> dict:
        # 1. Busca o usuário pelo e-mail
        user = self.user_repository.get_by_email(dto.email)
        if not user or not user.is_active:
            raise ValueError("Credenciais inválidas") # Mensagem genérica por segurança

        # 2. Verifica a senha (usando a mesma lógica do registro)
        if not verify_password(dto.password, user.password_hash):
            raise ValueError("Credenciais inválidas")

        # 3. Registra o último login
        user.register_login()
        self.user_repository.save(user)

        # 4. Retorna o Token (Simulado por enquanto - Dívida Técnica para JWT real)
        return {
            "access_token": create_access_token(user.id),
            "token_type": "bearer"
        }