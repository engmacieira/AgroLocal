import uuid
from typing import List, Optional
from dataclasses import dataclass
from app.domain.entities.producer_profile import ProducerProfile
from app.domain.repositories.producer_repository import IProducerRepository

@dataclass
class CreateProducerDTO:
    user_id: uuid.UUID
    store_name: str
    document: str
    pix_key: str
    bio: Optional[str] = None
    cover_image: Optional[str] = None

class CreateProducerUseCase:
    """Caso de Uso: Regista um utilizador como produtor."""
    def __init__(self, producer_repository: IProducerRepository):
        self.producer_repository = producer_repository

    def execute(self, dto: CreateProducerDTO) -> ProducerProfile:
        # 1. Regra: Um utilizador só pode ter 1 perfil
        existente = self.producer_repository.get_by_user_id(dto.user_id)
        if existente:
            raise ValueError("Usuário já possui um perfil de produtor ativo")
            
        # 2. Regra: CPF/CNPJ deve ser único
        doc_existente = self.producer_repository.get_by_document(dto.document)
        if doc_existente:
            raise ValueError("Este CPF/CNPJ já está registado em outro perfil")

        novo_perfil = ProducerProfile(
            user_id=dto.user_id,
            store_name=dto.store_name,
            document=dto.document,
            pix_key=dto.pix_key,
            bio=dto.bio,
            cover_image=dto.cover_image
        )
        return self.producer_repository.save(novo_perfil)

@dataclass
class UpdateProducerDTO:
    user_id: uuid.UUID # Buscamos pelo user_id para garantir que o dono está a editar
    store_name: Optional[str] = None
    bio: Optional[str] = None
    pix_key: Optional[str] = None

class UpdateProducerUseCase:
    """Caso de Uso: Atualiza os dados da vitrine ou financeiro."""
    def __init__(self, producer_repository: IProducerRepository):
        self.producer_repository = producer_repository

    def execute(self, dto: UpdateProducerDTO) -> ProducerProfile:
        perfil = self.producer_repository.get_by_user_id(dto.user_id)
        if not perfil:
            raise ValueError("Perfil de produtor não encontrado")

        perfil.update_details(
            new_name=dto.store_name,
            new_bio=dto.bio,
            new_pix_key=dto.pix_key
        )
        return self.producer_repository.save(perfil)

class GetProducerUseCase:
    """Caso de Uso: Busca o perfil pelo ID do utilizador."""
    def __init__(self, producer_repository: IProducerRepository):
        self.producer_repository = producer_repository

    def execute(self, user_id: uuid.UUID) -> ProducerProfile:
        perfil = self.producer_repository.get_by_user_id(user_id)
        if not perfil:
            raise ValueError("Perfil não encontrado")
        return perfil
    
class GetAllProducersUseCase:
    """Caso de Uso: Lista todos os produtores ativos para a vitrine."""
    def __init__(self, producer_repository: IProducerRepository):
        self.producer_repository = producer_repository

    def execute(self, skip: int = 0, limit: int = 100) -> List[ProducerProfile]:
        return self.producer_repository.get_all_active(skip, limit)

class DeleteProducerUseCase:
    """Caso de Uso: Desativa a vitrine de um produtor (Soft Delete)."""
    def __init__(self, producer_repository: IProducerRepository):
        self.producer_repository = producer_repository

    def execute(self, profile_id: uuid.UUID) -> None:
        self.producer_repository.delete(profile_id)