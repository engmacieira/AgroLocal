import pytest
import uuid
from typing import List, Optional
from app.domain.entities.address import Address, AddressType
from app.domain.repositories.address_repository import IAddressRepository
from app.application.use_cases.address_management import (
    CreateAddressUseCase, CreateAddressDTO,
    GetAddressesUseCase, DeleteAddressUseCase
)

# 1. O Dublê de Testes (Fake Repository)
class FakeAddressRepository(IAddressRepository):
    def __init__(self):
        self.addresses: List[Address] = []

    def save(self, address: Address) -> Address:
        existing = self.get_by_id(address.id)
        if existing:
            self.addresses.remove(existing)
        self.addresses.append(address)
        return address

    def get_by_id(self, address_id: uuid.UUID) -> Optional[Address]:
        return next((a for a in self.addresses if a.id == address_id), None)

    def get_by_user_id(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Address]:
        return [a for a in self.addresses if a.user_id == user_id and a.is_active is True]

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Address]:
        ativas = [a for a in self.addresses if a.is_active is True]
        return ativas[skip : skip + limit]
    
    def delete(self, address_id: uuid.UUID) -> None:
        address = self.get_by_id(address_id)
        if address:
            address.deactivate()

# 2. Testes dos Casos de Uso

def test_deve_criar_novo_endereco_via_caso_de_uso():
    fake_repo = FakeAddressRepository()
    use_case = CreateAddressUseCase(fake_repo)
    
    dto = CreateAddressDTO(
        user_id=uuid.uuid4(),
        address_type=AddressType.COMERCIAL,
        street="Avenida Central",
        number="1000",
        neighborhood="Centro",
        city="Lisboa",
        state="LX",
        postal_code="1000-001"
    )
    
    resultado = use_case.execute(dto)
    
    assert resultado is not None
    assert resultado.street == "Avenida Central"
    assert resultado.address_type == AddressType.COMERCIAL
    assert len(fake_repo.addresses) == 1

def test_deve_listar_apenas_enderecos_ativos_do_utilizador():
    fake_repo = FakeAddressRepository()
    user_id = uuid.uuid4()
    
    # Adicionamos dois endereços para o mesmo utilizador
    end1 = Address(user_id=user_id, street="Rua A", number="1", neighborhood="B", city="C", state="S", postal_code="0")
    end2 = Address(user_id=user_id, street="Rua B", number="2", neighborhood="B", city="C", state="S", postal_code="0")
    fake_repo.save(end1)
    fake_repo.save(end2)
    
    # Desativamos o primeiro
    end1.deactivate()
    
    use_case = GetAddressesUseCase(fake_repo)
    lista = use_case.execute(user_id)
    
    # Deve retornar apenas 1 endereço (o ativo)
    assert len(lista) == 1
    assert lista[0].street == "Rua B"

def test_deve_deletar_endereco_via_caso_de_uso():
    fake_repo = FakeAddressRepository()
    user_id = uuid.uuid4()
    endereco = Address(user_id=user_id, street="Rua X", number="1", neighborhood="B", city="C", state="S", postal_code="0")
    fake_repo.save(endereco)
    
    use_case = DeleteAddressUseCase(fake_repo)
    use_case.execute(endereco.id)
    
    assert endereco.is_active is False