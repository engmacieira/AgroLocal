from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.producer_product_repository_impl import ProducerProductRepositoryImpl
from app.application.use_cases.offer_management import (
    CreateOfferUseCase, CreateOfferDTO,
    UpdateStockUseCase, UpdateOfferUseCase, UpdateOfferDTO,
    GetProducerOffersUseCase, UpdateDeliveryOptionsUseCase, 
    DeliveryOptionDTO, AddOfferImageUseCase
)
from app.presentation.schemas.offer_schema import (
    OfferCreateRequest, OfferResponse, OfferStockUpdateRequest, 
    OfferUpdateRequest, DeliveryOptionsUpdateRequest, OfferImageAddRequest
)

router = APIRouter(prefix="/offers", tags=["Offers"])

@router.post("/", response_model=OfferResponse, status_code=status.HTTP_201_CREATED)
def create_offer(request: OfferCreateRequest, db: Session = Depends(get_db)):
    """O Produtor publica um item na sua vitrine."""
    repo = ProducerProductRepositoryImpl(db)
    use_case = CreateOfferUseCase(repo)
    
    dto = CreateOfferDTO(**request.model_dump())
    try:
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{offer_id}/stock", response_model=OfferResponse)
def update_stock(offer_id: UUID, request: OfferStockUpdateRequest, db: Session = Depends(get_db)):
    """Atualiza o estoque atual de uma oferta (Aceita valor negativo para baixa)."""
    repo = ProducerProductRepositoryImpl(db)
    use_case = UpdateStockUseCase(repo)
    try:
        return use_case.execute(offer_id, request.add_quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{offer_id}/details", response_model=OfferResponse)
def update_offer_details(offer_id: UUID, request: OfferUpdateRequest, db: Session = Depends(get_db)):
    """Altera preço ou descrição de um produto já ofertado."""
    repo = ProducerProductRepositoryImpl(db)
    use_case = UpdateOfferUseCase(repo)
    
    dto = UpdateOfferDTO(offer_id=offer_id, **request.model_dump(exclude_unset=True))
    try:
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/producer/{producer_id}", response_model=List[OfferResponse])
def get_producer_offers(producer_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista a vitrine de ofertas ativas de um determinado produtor."""
    repo = ProducerProductRepositoryImpl(db)
    use_case = GetProducerOffersUseCase(repo)
    return use_case.execute(producer_id, skip, limit)

@router.put("/{offer_id}/delivery", response_model=OfferResponse)
def update_delivery_options(offer_id: UUID, request: DeliveryOptionsUpdateRequest, db: Session = Depends(get_db)):
    """Substitui a grade de opções de entrega/retirada de uma oferta."""
    repo = ProducerProductRepositoryImpl(db)
    use_case = UpdateDeliveryOptionsUseCase(repo)
    
    # Converte de Request Schema para DTO
    dtos = [DeliveryOptionDTO(**opt.model_dump()) for opt in request.options]
    
    try:
        return use_case.execute(offer_id, dtos)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{offer_id}/images", response_model=OfferResponse)
def add_offer_image(offer_id: UUID, request: OfferImageAddRequest, db: Session = Depends(get_db)):
    """Anexa uma foto real da colheita à oferta."""
    repo = ProducerProductRepositoryImpl(db)
    use_case = AddOfferImageUseCase(repo)
    try:
        return use_case.execute(offer_id, request.url, request.is_primary)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))