from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.producer_repository_impl import ProducerRepositoryImpl
from app.application.use_cases.producer_management import (
    CreateProducerUseCase, CreateProducerDTO,
    UpdateProducerUseCase, UpdateProducerDTO,
    GetProducerUseCase, GetAllProducersUseCase, DeleteProducerUseCase
)
from app.presentation.schemas.producer_schema import (
    ProducerCreateRequest, ProducerUpdateRequest, ProducerResponse
)

router = APIRouter(prefix="/producers", tags=["Producers"])

@router.post("/", response_model=ProducerResponse, status_code=status.HTTP_201_CREATED)
def create_producer(request: ProducerCreateRequest, db: Session = Depends(get_db)):
    """Regista um utilizador como produtor/vendedor."""
    repo = ProducerRepositoryImpl(db)
    use_case = CreateProducerUseCase(repo)
    
    dto = CreateProducerDTO(**request.model_dump())
    try:
        return use_case.execute(dto)
    except ValueError as e:
        # Se o CPF já existir ou o utilizador já for produtor
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/user/{user_id}", response_model=ProducerResponse)
def get_producer(user_id: UUID, db: Session = Depends(get_db)):
    """Busca a vitrine de um produtor específico."""
    repo = ProducerRepositoryImpl(db)
    use_case = GetProducerUseCase(repo)
    try:
        return use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/user/{user_id}", response_model=ProducerResponse)
def update_producer(user_id: UUID, request: ProducerUpdateRequest, db: Session = Depends(get_db)):
    """Atualiza as informações públicas da loja."""
    repo = ProducerRepositoryImpl(db)
    use_case = UpdateProducerUseCase(repo)
    
    update_data = request.model_dump(exclude_unset=True)
    dto = UpdateProducerDTO(user_id=user_id, **update_data)
    
    try:
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get("/", response_model=List[ProducerResponse])
def get_all_producers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os produtores ativos (Vitrine do Marketplace)."""
    repo = ProducerRepositoryImpl(db)
    use_case = GetAllProducersUseCase(repo)
    return use_case.execute(skip, limit)

@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producer(profile_id: UUID, db: Session = Depends(get_db)):
    """Desativa um perfil de produtor (Soft Delete)."""
    repo = ProducerRepositoryImpl(db)
    use_case = DeleteProducerUseCase(repo)
    use_case.execute(profile_id)