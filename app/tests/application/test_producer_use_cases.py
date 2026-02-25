import pytest
import uuid
from typing import List, Optional
from app.domain.entities.producer_profile import ProducerProfile
from app.domain.repositories.producer_repository import IProducerRepository
from app.application.use_cases.producer_management import (
    CreateProducerUseCase, CreateProducerDTO,
    UpdateProducerUseCase, UpdateProducerDTO,
    GetProducerUseCase
)

# 1. O Dublê de Testes Completo
class FakeProducerRepository(IProducerRepository):
    def __init__(self):
        self.profiles: List[ProducerProfile] = []

    def save(self, profile: ProducerProfile) -> ProducerProfile:
        existing = self.get_by_id(profile.id)
        if existing:
            self.profiles.remove(existing)
        self.profiles.append(profile)
        return profile

    def get_by_id(self, profile_id: uuid.UUID) -> Optional[ProducerProfile]:
        return next((p for p in self.profiles if p.id == profile_id), None)

    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[ProducerProfile]:
        return next((p for p in self.profiles if p.user_id == user_id and p.is_active), None)

    def get_by_document(self, document: str) -> Optional[ProducerProfile]:
        return next((p for p in self.profiles if p.document == document), None)

    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[ProducerProfile]:
        ativas = [p for p in self.profiles if p.is_active]
        return ativas[skip : skip + limit]

    def delete(self, profile_id: uuid.UUID) -> None:
        profile = self.get_by_id(profile_id)
        if profile:
            profile.deactivate()

# 2. Testes de Casos de Uso

def test_deve_criar_novo_perfil_de_produtor():
    fake_repo = FakeProducerRepository()
    use_case = CreateProducerUseCase(fake_repo)
    user_id = uuid.uuid4()
    
    dto = CreateProducerDTO(
        user_id=user_id,
        store_name="Horta do Zé",
        document="12345678901",
        pix_key="ze@pix.com"
    )
    
    resultado = use_case.execute(dto)
    
    assert resultado.store_name == "Horta do Zé"
    assert resultado.rating == 5.0
    assert fake_repo.get_by_user_id(user_id) is not None

def test_nao_deve_permitir_dois_perfis_para_mesmo_usuario():
    fake_repo = FakeProducerRepository()
    use_case = CreateProducerUseCase(fake_repo)
    user_id = uuid.uuid4()
    
    # Cria o primeiro
    use_case.execute(CreateProducerDTO(user_id=user_id, store_name="Loja 1", document="111", pix_key="pix1"))
    
    # Tenta criar o segundo para o MESMO user_id
    with pytest.raises(ValueError, match="Usuário já possui um perfil de produtor ativo"):
        use_case.execute(CreateProducerDTO(user_id=user_id, store_name="Loja 2", document="222", pix_key="pix2"))

def test_nao_deve_permitir_documentos_duplicados():
    fake_repo = FakeProducerRepository()
    use_case = CreateProducerUseCase(fake_repo)
    
    # Cria com documento "999"
    use_case.execute(CreateProducerDTO(user_id=uuid.uuid4(), store_name="A", document="999", pix_key="A"))
    
    # Tenta criar outro perfil com o mesmo documento "999"
    with pytest.raises(ValueError, match="Este CPF/CNPJ já está registado em outro perfil"):
        use_case.execute(CreateProducerDTO(user_id=uuid.uuid4(), store_name="B", document="999", pix_key="B"))