import pytest
from app.domain.entities.producer_profile import ProducerProfile
from app.domain.entities.user import User
from app.infrastructure.repositories.producer_repository_impl import ProducerRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

def test_deve_salvar_e_buscar_perfil_de_produtor(db_session):
    # 1. Cria o utilizador base (FK Obrigatória)
    user_repo = UserRepositoryImpl(db_session)
    user = User(email="produtor.novo@agrolocal.com", password_hash="123", full_name="João Produtor")
    user_repo.save(user)

    # 2. Cria o Perfil de Produtor
    repo = ProducerRepositoryImpl(db_session)
    perfil = ProducerProfile(
        user_id=user.id,
        store_name="Fazenda Esperança",
        document="11122233344",
        pix_key="chavepix@email.com",
        bio="Hortaliças frescas"
    )
    
    # 3. Act
    repo.save(perfil)
    perfil_salvo = repo.get_by_user_id(user.id)
    
    # 4. Assert
    assert perfil_salvo is not None
    assert perfil_salvo.store_name == "Fazenda Esperança"
    assert perfil_salvo.rating == 5.0 # Valida o valor default a chegar da base de dados!