import uuid
from typing import List, Optional
from dataclasses import dataclass
from app.domain.entities.address import Address, AddressType
from app.domain.repositories.address_repository import IAddressRepository

@dataclass
class CreateAddressDTO:
    """DTO com os dados necessários para criar um endereço."""
    user_id: uuid.UUID
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
    
    address_type: AddressType = AddressType.RESIDENCIAL
    label: Optional[str] = None
    complement: Optional[str] = None
    reference_point: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CreateAddressUseCase:
    """Caso de Uso: Adicionar um novo endereço ao utilizador."""
    def __init__(self, address_repository: IAddressRepository):
        self.address_repository = address_repository

    def execute(self, dto: CreateAddressDTO) -> Address:
        novo_endereco = Address(
            user_id=dto.user_id,
            address_type=dto.address_type,
            label=dto.label,
            street=dto.street,
            number=dto.number,
            complement=dto.complement,
            neighborhood=dto.neighborhood,
            city=dto.city,
            state=dto.state,
            postal_code=dto.postal_code,
            reference_point=dto.reference_point,
            latitude=dto.latitude,
            longitude=dto.longitude
        )
        return self.address_repository.save(novo_endereco)

class GetAddressesUseCase:
    """Caso de Uso: Buscar todos os endereços ativos de um utilizador."""
    def __init__(self, address_repository: IAddressRepository):
        self.address_repository = address_repository

    def execute(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Address]:
        return self.address_repository.get_by_user_id(user_id, skip, limit)

class DeleteAddressUseCase:
    """Caso de Uso: Remover (Soft Delete) um endereço do catálogo."""
    def __init__(self, address_repository: IAddressRepository):
        self.address_repository = address_repository

    def execute(self, address_id: uuid.UUID) -> None:
        endereco = self.address_repository.get_by_id(address_id)
        if not endereco:
            raise ValueError("Endereço não encontrado")
            
        self.address_repository.delete(address_id)
        
@dataclass
class UpdateAddressDTO:
    """DTO com os dados opcionais para atualização."""
    address_id: uuid.UUID
    label: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    reference_point: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UpdateAddressUseCase:
    """Caso de Uso: Atualizar dados de um endereço existente."""
    def __init__(self, address_repository: IAddressRepository):
        self.address_repository = address_repository

    def execute(self, dto: UpdateAddressDTO) -> Address:
        endereco = self.address_repository.get_by_id(dto.address_id)
        if not endereco or not endereco.is_active:
            raise ValueError("Endereço não encontrado ou inativo")

        # Atualiza dinamicamente apenas os campos que foram enviados
        for field, value in vars(dto).items():
            if value is not None and field != 'address_id':
                setattr(endereco, field, value)

        return self.address_repository.save(endereco)

class GetAllAddressesUseCase:
    """Caso de Uso: Listar todos os endereços do sistema."""
    def __init__(self, address_repository: IAddressRepository):
        self.address_repository = address_repository

    def execute(self, skip: int = 0, limit: int = 100) -> List[Address]:
        return self.address_repository.get_all(skip, limit)