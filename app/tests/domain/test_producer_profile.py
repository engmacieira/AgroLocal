import pytest
import uuid
from app.domain.entities.producer_profile import ProducerProfile

def test_deve_criar_perfil_de_produtor_com_sucesso():
    # Arrange
    user_id = uuid.uuid4()
    
    # Act
    perfil = ProducerProfile(
        user_id=user_id,
        store_name="Fazenda Sol Nascente",
        document="12345678901",
        pix_key="fazenda@email.com",
        bio="Produtos orgânicos direto da roça."
    )

    # Assert
    assert perfil.user_id == user_id
    assert perfil.store_name == "Fazenda Sol Nascente"
    assert perfil.rating == 5.0  # Começa sem avaliações
    assert perfil.is_active is True

def test_deve_permitir_atualizar_bio_e_loja():
    # Arrange
    perfil = ProducerProfile(
        user_id=uuid.uuid4(),
        store_name="Loja A",
        document="000",
        pix_key="key"
    )

    # Act
    perfil.update_details(
        new_name="Lojinha do Matheus",
        new_bio="Nova descrição"
    )

    # Assert
    assert perfil.store_name == "Lojinha do Matheus"
    assert perfil.bio == "Nova descrição"

def test_deve_desativar_perfil_produtor():
    perfil = ProducerProfile(
        user_id=uuid.uuid4(),
        store_name="Temp",
        document="0",
        pix_key="0"
    )
    
    perfil.deactivate()
    
    assert perfil.is_active is False