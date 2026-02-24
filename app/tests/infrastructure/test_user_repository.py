import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.domain.entities.user import User, UserRole
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

# 1. Configuração (Fixture): Cria um banco "fake" na memória RAM
@pytest.fixture
def db_session():
    # Cria motor na memória
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    
    # Cria todas as tabelas mapeadas pela classe Base (ex: UserModel)
    Base.metadata.create_all(bind=engine)
    
    # Inicia a sessão
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session  # Entrega a sessão para o teste usar
    
    # Limpa tudo após o teste
    session.close()
    Base.metadata.drop_all(bind=engine)

# 2. Teste: Salvar e Buscar
def test_deve_salvar_e_buscar_usuario_por_id(db_session):
    # Arrange
    repo = UserRepositoryImpl(db_session)
    novo_usuario = User(
        email="teste_infra@agrolocal.com",
        password_hash="hash_super_secreto",
        full_name="Agricultor Teste",
        role=UserRole.PRODUTOR
    )
    
    # Act - Salvando no banco
    repo.save(novo_usuario)
    
    # Act - Buscando do banco
    usuario_recuperado = repo.get_by_id(novo_usuario.id)
    
    # Assert
    assert usuario_recuperado is not None
    assert usuario_recuperado.email == "teste_infra@agrolocal.com"
    assert usuario_recuperado.is_active is True
    assert usuario_recuperado.role == UserRole.PRODUTOR

# 3. Teste: Regra de Soft Delete
def test_deve_aplicar_soft_delete_corretamente(db_session):
    # Arrange
    repo = UserRepositoryImpl(db_session)
    usuario = User(
        email="deletar@agrolocal.com", 
        password_hash="123", 
        full_name="Deletado"
    )
    repo.save(usuario) # Salva ativo (is_active=True)
    
    # Act - Dispara o delete
    repo.delete(usuario.id)
    
    # Assert
    usuario_atualizado = repo.get_by_id(usuario.id)
    assert usuario_atualizado is not None
    assert usuario_atualizado.is_active is False, "A regra de negócio 'deactivate()' deve refletir no banco"