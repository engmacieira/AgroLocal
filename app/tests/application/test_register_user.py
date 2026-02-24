import pytest
from uuid import UUID
from typing import Optional
from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import IUserRepository

# 1. O Dublê de Testes (Fake Repository)
# Ele finge ser o banco de dados, mas guarda tudo numa lista na memória RAM
class FakeUserRepository(IUserRepository):
    def __init__(self):
        self.users = []

    def save(self, user: User) -> User:
        # Lógica de Update ou Insert simulada
        existing = self.get_by_id(user.id)
        if existing:
            self.users.remove(existing)
        self.users.append(user)
        return user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return next((u for u in self.users if u.id == user_id), None)

    def get_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self.users if u.email == email), None)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.users[skip : skip + limit]

    def delete(self, user_id: UUID) -> None:
        user = self.get_by_id(user_id)
        if user:
            user.deactivate()
            
# Vamos importar o Caso de Uso e o DTO (que ainda não existem, por isso vai falhar!)
from app.application.use_cases.register_user import RegisterUserUseCase, RegisterUserDTO

# 2. O Teste de Sucesso
def test_deve_registrar_um_novo_usuario_com_sucesso():
    # Arrange
    fake_repo = FakeUserRepository()
    use_case = RegisterUserUseCase(user_repository=fake_repo)
    
    # DTO (Data Transfer Object) - Os dados crus que vêm de fora (ex: da API)
    dto = RegisterUserDTO(
        email="novo@agrolocal.com",
        password="senha_em_texto_plano",
        full_name="João Novo",
        role=UserRole.PRODUTOR
    )
    
    # Act
    resultado = use_case.execute(dto)
    
    # Assert
    assert resultado is not None
    assert resultado.email == "novo@agrolocal.com"
    # A senha NUNCA deve ser salva em texto plano! O Caso de Uso deve ter feito o hash.
    assert resultado.password_hash != "senha_em_texto_plano"
    
    # Verifica se realmente foi salvo no nosso "banco fake"
    usuario_no_banco = fake_repo.get_by_email("novo@agrolocal.com")
    assert usuario_no_banco is not None

# 3. O Teste de Falha (Regra de Negócio: E-mail Único)
def test_nao_deve_permitir_registrar_usuario_com_email_duplicado():
    # Arrange
    fake_repo = FakeUserRepository()
    # Injetamos um usuário que "já existe" no banco fake
    fake_repo.save(User(email="existente@agrolocal.com", password_hash="hash", full_name="Antigo"))
    
    use_case = RegisterUserUseCase(user_repository=fake_repo)
    dto = RegisterUserDTO(
        email="existente@agrolocal.com", # Mesmo e-mail!
        password="123",
        full_name="Copião"
    )
    
    # Act & Assert
    # Esperamos que o Caso de Uso levante um erro (Exception)
    with pytest.raises(ValueError, match="Email já está em uso"):
        use_case.execute(dto)