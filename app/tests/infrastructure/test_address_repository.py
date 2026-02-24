import pytest
import uuid
from app.domain.entities.address import Address, AddressType
from app.domain.entities.user import User
from app.infrastructure.repositories.address_repository_impl import AddressRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

def test_deve_salvar_e_buscar_endereco(db_session):
    # 1. Arrange - Precisamos de um User válido primeiro por causa da Foreign Key
    user_repo = UserRepositoryImpl(db_session)
    user = User(email="dono_endereco@agrolocal.com", password_hash="123", full_name="João")
    user_repo.save(user)

    # 2. Arrange - O Endereço
    repo = AddressRepositoryImpl(db_session)
    novo_endereco = Address(
        user_id=user.id,
        address_type=AddressType.RURAL,
        street="Estrada Velha",
        number="S/N",
        neighborhood="Zona Rural",
        city="Interior",
        state="SP",
        postal_code="12345-000",
        reference_point="Perto do rio"
    )
    
    # 3. Act
    repo.save(novo_endereco)
    enderecos_do_utilizador = repo.get_by_user_id(user.id)
    endereco_recuperado = repo.get_by_id(novo_endereco.id)
    
    # 4. Assert
    assert endereco_recuperado is not None
    assert endereco_recuperado.city == "Interior"
    assert len(enderecos_do_utilizador) == 1
    assert enderecos_do_utilizador[0].id == novo_endereco.id

def test_soft_delete_deve_esconder_endereco_da_lista(db_session):
    # 1. Arrange
    user_repo = UserRepositoryImpl(db_session)
    user = User(email="deletar_end@agrolocal.com", password_hash="123", full_name="Maria")
    user_repo.save(user)

    repo = AddressRepositoryImpl(db_session)
    endereco = Address(
        user_id=user.id, street="Rua A", number="1", neighborhood="B", 
        city="C", state="SP", postal_code="000"
    )
    repo.save(endereco)
    
    # 2. Act - Desativar
    repo.delete(endereco.id)
    
    # 3. Assert - get_by_user_id não deve retornar endereços inativos
    enderecos_ativos = repo.get_by_user_id(user.id)
    assert len(enderecos_ativos) == 0