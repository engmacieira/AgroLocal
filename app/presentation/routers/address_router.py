from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.address_repository_impl import AddressRepositoryImpl
from app.application.use_cases.address_management import (
    CreateAddressUseCase, CreateAddressDTO,
    GetAddressesUseCase, DeleteAddressUseCase,
    UpdateAddressUseCase, UpdateAddressDTO, GetAllAddressesUseCase
)
from app.presentation.schemas.address_schema import AddressCreateRequest, AddressResponse, AddressUpdateRequest

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(request: AddressCreateRequest, db: Session = Depends(get_db)):
    """Regista um novo endereço para um utilizador."""
    repo = AddressRepositoryImpl(db)
    use_case = CreateAddressUseCase(repo)
    
    # Mapeamos o Request do Pydantic diretamente para o nosso DTO da Aplicação
    dto = CreateAddressDTO(**request.model_dump())
    
    try:
        return use_case.execute(dto)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/user/{user_id}", response_model=List[AddressResponse])
def get_user_addresses(user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os endereços ativos de um utilizador específico."""
    repo = AddressRepositoryImpl(db)
    use_case = GetAddressesUseCase(repo)
    return use_case.execute(user_id, skip, limit)

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: UUID, db: Session = Depends(get_db)):
    """Desativa um endereço (Soft Delete)."""
    repo = AddressRepositoryImpl(db)
    use_case = DeleteAddressUseCase(repo)
    try:
        use_case.execute(address_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get("/", response_model=List[AddressResponse])
def get_all_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os endereços do sistema (Visão Geral/Admin)."""
    repo = AddressRepositoryImpl(db)
    use_case = GetAllAddressesUseCase(repo)
    return use_case.execute(skip, limit)

@router.put("/{address_id}", response_model=AddressResponse)
def update_address(address_id: UUID, request: AddressUpdateRequest, db: Session = Depends(get_db)):
    """Atualiza dados de um endereço existente."""
    repo = AddressRepositoryImpl(db)
    use_case = UpdateAddressUseCase(repo)
    
    # Excluímos os valores None para não sobrescrever dados existentes com nulos
    update_data = request.model_dump(exclude_unset=True)
    dto = UpdateAddressDTO(address_id=address_id, **update_data)
    
    try:
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))