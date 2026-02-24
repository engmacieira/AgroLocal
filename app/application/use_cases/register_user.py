import hashlib
from dataclasses import dataclass
from typing import Optional
from app.core.security import get_password_hash
from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import IUserRepository

@dataclass
class RegisterUserDTO:
    """
    DTO (Data Transfer Object)
    Representa os dados crus necessários para registrar um usuário.
    É o contrato de entrada do Caso de Uso.
    """
    email: str
    password: str  # Senha em texto plano que vem do usuário
    full_name: str
    role: UserRole = UserRole.CLIENTE
    phone: Optional[str] = None

class RegisterUserUseCase:
    """
    Caso de Uso: Registrar um novo usuário no sistema.
    Orquestra a validação, segurança e persistência.
    """
    
    # Injeção de Dependência: O caso de uso pede o CONTRATO (Interface), 
    # não se importando se é o banco fake dos testes ou o banco real SQLAlchemy.
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, dto: RegisterUserDTO) -> User:
        # 1. Validação de Regra de Negócio: E-mail único
        usuario_existente = self.user_repository.get_by_email(dto.email)
        if usuario_existente:
            raise ValueError("Email já está em uso")

        # 2. Segurança: Gerar o Hash da Senha
        hashed_password = get_password_hash(dto.password)

        # 3. Criação da Entidade de Domínio
        novo_usuario = User(
            email=dto.email,
            password_hash=hashed_password,
            full_name=dto.full_name,
            role=dto.role,
            phone=dto.phone
        )

        # 4. Persistência (Manda o repositório salvar)
        usuario_salvo = self.user_repository.save(novo_usuario)

        return usuario_salvo