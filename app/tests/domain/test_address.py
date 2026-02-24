import pytest
import uuid
from datetime import datetime
from app.domain.entities.address import Address, AddressType

def test_criar_endereco_urbano_com_sucesso():
    # Arrange & Act
    user_id = uuid.uuid4()
    endereco = Address(
        user_id=user_id,
        address_type=AddressType.RESIDENCIAL,
        label="Minha Casa",
        street="Rua das Flores",
        number="123",
        neighborhood="Centro",
        city="São Paulo",
        state="SP",
        postal_code="01000-000"
    )

    # Assert
    assert isinstance(endereco.id, uuid.UUID)
    assert endereco.user_id == user_id
    assert endereco.address_type == AddressType.RESIDENCIAL
    assert endereco.is_active is True, "Um novo endereço deve nascer ativo"
    assert endereco.is_default is False, "Não deve nascer como padrão automaticamente"

def test_criar_endereco_rural_com_coordenadas_e_referencia():
    # Arrange & Act
    endereco = Address(
        user_id=uuid.uuid4(),
        address_type=AddressType.RURAL,
        label="Sítio Esperança",
        street="Estrada de Terra",
        number="S/N",
        neighborhood="Zona Rural",
        city="Ibiúna",
        state="SP",
        postal_code="18150-000",
        reference_point="Após a ponte de madeira, porteira azul",
        latitude=-23.654321,
        longitude=-47.123456
    )

    # Assert
    assert endereco.reference_point is not None
    assert endereco.latitude == -23.654321
    assert endereco.longitude == -47.123456

def test_endereco_pode_ser_definido_como_padrao():
    # Arrange
    endereco = Address(
        user_id=uuid.uuid4(),
        street="Rua A", number="1", neighborhood="Bairro", 
        city="Cidade", state="SP", postal_code="00000-000"
    )
    assert endereco.is_default is False

    # Act
    endereco.set_as_default()

    # Assert
    assert endereco.is_default is True

def test_endereco_pode_ser_desativado_soft_delete():
    # Arrange
    endereco = Address(
        user_id=uuid.uuid4(),
        street="Rua B", number="2", neighborhood="Bairro", 
        city="Cidade", state="SP", postal_code="00000-000"
    )
    
    # Act
    endereco.deactivate()

    # Assert
    assert endereco.is_active is False